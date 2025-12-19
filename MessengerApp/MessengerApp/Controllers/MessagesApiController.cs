using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using MessengerApp.Data;
using MessengerApp.Models;
using Microsoft.AspNetCore.Authorization;
using System.Security.Claims;
using System.ComponentModel.DataAnnotations;

namespace MessengerApp.Controllers
{
    [Route("api/[controller]")]
    [ApiController]
    [Authorize]
    public class MessagesApiController : ControllerBase
    {
        private readonly ApplicationDbContext _context;
        private readonly ILogger<MessagesApiController> _logger;

        public MessagesApiController(ApplicationDbContext context, ILogger<MessagesApiController> logger)
        {
            _context = context;
            _logger = logger;
        }

        // GET: api/MessagesApi
        [HttpGet]
        public async Task<ActionResult<IEnumerable<MessageDto>>> GetMessages(
            [FromQuery] DateTime? startDate,
            [FromQuery] DateTime? endDate,
            [FromQuery] string? ipAddress,
            [FromQuery] bool groupByIp = false,
            [FromQuery] bool groupByDate = false,
            [FromQuery] string? receiverId = null)
        {
            try
            {
                var userId = User.FindFirstValue(ClaimTypes.NameIdentifier);
                var query = _context.Messages
                    .Include(m => m.Sender)
                    .Include(m => m.Receiver)
                    .Where(m => m.SenderId == userId || m.ReceiverId == userId);

                // Фильтрация по получателю
                if (!string.IsNullOrEmpty(receiverId))
                {
                    query = query.Where(m =>
                        (m.SenderId == userId && m.ReceiverId == receiverId) ||
                        (m.SenderId == receiverId && m.ReceiverId == userId));
                }

                // Фильтрация по дате
                if (startDate.HasValue)
                {
                    query = query.Where(m => m.SentAt >= startDate.Value);
                }
                if (endDate.HasValue)
                {
                    query = query.Where(m => m.SentAt <= endDate.Value);
                }

                // Фильтрация по IP
                if (!string.IsNullOrEmpty(ipAddress))
                {
                    query = query.Where(m => m.SenderIP == ipAddress);
                }

                // Группировка
                if (groupByIp)
                {
                    var groupedByIp = await query
                        .GroupBy(m => m.SenderIP)
                        .Select(g => new
                        {
                            IPAddress = g.Key,
                            MessageCount = g.Count(),
                            FirstMessage = g.Min(m => m.SentAt),
                            LastMessage = g.Max(m => m.SentAt),
                            Messages = g.Select(m => new MessageDto(m)).ToList()
                        })
                        .ToListAsync();

                    return Ok(groupedByIp);
                }
                else if (groupByDate)
                {
                    var groupedByDate = await query
                        .GroupBy(m => m.SentAt.Date)
                        .Select(g => new
                        {
                            Date = g.Key,
                            MessageCount = g.Count(),
                            Messages = g.Select(m => new MessageDto(m)).ToList()
                        })
                        .OrderByDescending(g => g.Date)
                        .ToListAsync();

                    return Ok(groupedByDate);
                }
                else
                {
                    var messages = await query
                        .OrderBy(m => m.SentAt)
                        .Select(m => new MessageDto(m))
                        .ToListAsync();

                    return Ok(messages);
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error retrieving messages");
                return StatusCode(500, "Internal server error");
            }
        }

        // GET: api/MessagesApi/5
        [HttpGet("{id}")]
        public async Task<ActionResult<MessageDto>> GetMessage(int id)
        {
            var userId = User.FindFirstValue(ClaimTypes.NameIdentifier);
            var message = await _context.Messages
                .Include(m => m.Sender)
                .Include(m => m.Receiver)
                .FirstOrDefaultAsync(m => m.Id == id &&
                    (m.SenderId == userId || m.ReceiverId == userId));

            if (message == null)
            {
                return NotFound();
            }

            return new MessageDto(message);
        }

        // POST: api/MessagesApi
        [HttpPost]
        public async Task<ActionResult<MessageDto>> PostMessage([FromBody] CreateMessageDto messageDto)
        {
            if (!ModelState.IsValid)
            {
                return BadRequest(ModelState);
            }

            var userId = User.FindFirstValue(ClaimTypes.NameIdentifier);
            var ipAddress = HttpContext.Connection.RemoteIpAddress?.ToString();

            // Проверяем, существует ли получатель
            var receiverExists = await _context.Users.AnyAsync(u => u.Id == messageDto.ReceiverId);
            if (!receiverExists)
            {
                return BadRequest("Receiver not found");
            }

            var message = new Message
            {
                SenderId = userId,
                ReceiverId = messageDto.ReceiverId,
                Content = messageDto.Content,
                SenderIP = ipAddress,
                SentAt = DateTime.UtcNow
            };

            _context.Messages.Add(message);
            await _context.SaveChangesAsync();

            // Загружаем связанные данные для DTO
            var savedMessage = await _context.Messages
                .Include(m => m.Sender)
                .Include(m => m.Receiver)
                .FirstOrDefaultAsync(m => m.Id == message.Id);

            // Логирование
            _logger.LogInformation($"Message sent from {userId} to {messageDto.ReceiverId} from IP: {ipAddress}");

            return CreatedAtAction("GetMessage", new { id = message.Id }, new MessageDto(savedMessage));
        }

        // DTO классы
        public class MessageDto
        {
            public int Id { get; set; }
            public string SenderId { get; set; }
            public string SenderName { get; set; }
            public string ReceiverId { get; set; }
            public string ReceiverName { get; set; }
            public string Content { get; set; }
            public DateTime SentAt { get; set; }
            public DateTime SentAtMoscow { get; set; }
            public bool IsRead { get; set; }
            public string SenderIP { get; set; }

            public MessageDto(Message message)
            {
                if (message == null)
                {
                    throw new ArgumentNullException(nameof(message));
                }

                Id = message.Id;
                SenderId = message.SenderId;
                ReceiverId = message.ReceiverId;
                Content = message.Content;
                SentAt = message.SentAt;
                SentAtMoscow = ConvertToMoscowTime(message.SentAt);
                IsRead = message.IsRead;
                SenderIP = message.SenderIP;

                // Безопасное получение имен
                SenderName = message.Sender != null
                    ? $"{message.Sender.FirstName} {message.Sender.LastName}"
                    : "Unknown Sender";

                ReceiverName = message.Receiver != null
                    ? $"{message.Receiver.FirstName} {message.Receiver.LastName}"
                    : "Unknown Receiver";
            }

            // Пустой конструктор для сериализации
            public MessageDto() { }

            // Статический метод для конвертации времени
            private static DateTime ConvertToMoscowTime(DateTime utcTime)
            {
                try
                {
                    // Пробуем получить московскую таймзону
                    var moscowTimeZone = TimeZoneInfo.FindSystemTimeZoneById("Russian Standard Time");
                    return TimeZoneInfo.ConvertTimeFromUtc(utcTime, moscowTimeZone);
                }
                catch
                {
                    try
                    {
                        // Для Linux/Mac
                        var moscowTimeZone = TimeZoneInfo.FindSystemTimeZoneById("Europe/Moscow");
                        return TimeZoneInfo.ConvertTimeFromUtc(utcTime, moscowTimeZone);
                    }
                    catch
                    {
                        return utcTime.AddHours(3);
                    }
                }
            }
        }

        public class CreateMessageDto
        {
            [Required]
            public string ReceiverId { get; set; }

            [Required]
            [MaxLength(5000)]
            public string Content { get; set; }
        }
    }
}
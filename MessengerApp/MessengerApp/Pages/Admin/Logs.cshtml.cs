using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using MessengerApp.Data;
using MessengerApp.ViewModels;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Authorization;

namespace MessengerApp.Pages.Admin
{
    [Authorize(Roles = "Admin")]
    public class LogsModel : PageModel
    {
        private readonly ApplicationDbContext _context;

        public LogsModel(ApplicationDbContext context)
        {
            _context = context;
        }

        [BindProperty(SupportsGet = true)]
        public LogFilterViewModel Filter { get; set; } = new LogFilterViewModel();

        public List<MessageViewModel> Messages { get; set; }
        public List<GroupedByIpViewModel> GroupedMessagesByIp { get; set; }
        public List<GroupedByDateViewModel> GroupedMessagesByDate { get; set; }
        public string ApiUrl { get; set; }

        public async Task OnGetAsync()
        {
            var query = _context.Messages
                .Include(m => m.Sender)
                .Include(m => m.Receiver)
                .AsQueryable();

            // Применяем фильтры
            if (Filter.StartDate.HasValue)
            {
                query = query.Where(m => m.SentAt >= Filter.StartDate.Value);
            }

            if (Filter.EndDate.HasValue)
            {
                query = query.Where(m => m.SentAt <= Filter.EndDate.Value);
            }

            if (!string.IsNullOrEmpty(Filter.IpAddress))
            {
                query = query.Where(m => m.SenderIP.Contains(Filter.IpAddress));
            }

            // Группировка
            if (Filter.GroupByIp)
            {
                GroupedMessagesByIp = await query
                    .GroupBy(m => m.SenderIP)
                    .Select(g => new GroupedByIpViewModel
                    {
                        IPAddress = g.Key,
                        MessageCount = g.Count(),
                        FirstMessage = g.Min(m => m.SentAt),
                        LastMessage = g.Max(m => m.SentAt)
                    })
                    .OrderByDescending(g => g.MessageCount)
                    .ToListAsync();
            }
            else if (Filter.GroupByDate)
            {
                GroupedMessagesByDate = await query
                    .GroupBy(m => m.SentAt.Date)
                    .Select(g => new GroupedByDateViewModel
                    {
                        Date = g.Key,
                        MessageCount = g.Count()
                    })
                    .OrderByDescending(g => g.Date)
                    .ToListAsync();
            }
            else
            {
                // Сортировка
                switch (Filter.SortBy)
                {
                    case "IP":
                        query = Filter.SortOrder == "Asc"
                            ? query.OrderBy(m => m.SenderIP)
                            : query.OrderByDescending(m => m.SenderIP);
                        break;
                    case "Sender":
                        query = Filter.SortOrder == "Asc"
                            ? query.OrderBy(m => m.Sender.FirstName)
                            : query.OrderByDescending(m => m.Sender.FirstName);
                        break;
                    default:
                        query = Filter.SortOrder == "Asc"
                            ? query.OrderBy(m => m.SentAt)
                            : query.OrderByDescending(m => m.SentAt);
                        break;
                }

                Messages = await query
                    .Select(m => new MessageViewModel
                    {
                        Id = m.Id,
                        SenderName = m.Sender.FirstName + " " + m.Sender.LastName,
                        ReceiverName = m.Receiver.FirstName + " " + m.Receiver.LastName,
                        ContentPreview = m.Content.Length > 50 ? m.Content.Substring(0, 50) + "..." : m.Content,
                        SentAt = m.SentAt,
                        IsRead = m.IsRead,
                        SenderIP = m.SenderIP
                    })
                    .ToListAsync();
            }

            // Генерация URL для API
            ApiUrl = $"/api/MessagesApi?startDate={Filter.StartDate:yyyy-MM-dd}&endDate={Filter.EndDate:yyyy-MM-dd}";
            if (!string.IsNullOrEmpty(Filter.IpAddress))
            {
                ApiUrl += $"&ipAddress={Filter.IpAddress}";
            }
            if (Filter.GroupByIp)
            {
                ApiUrl += "&groupByIp=true";
            }
            if (Filter.GroupByDate)
            {
                ApiUrl += "&groupByDate=true";
            }
        }
    }

    public class MessageViewModel
    {
        public int Id { get; set; }
        public string SenderName { get; set; }
        public string ReceiverName { get; set; }
        public string ContentPreview { get; set; }
        public DateTime SentAt { get; set; }
        public bool IsRead { get; set; }
        public string SenderIP { get; set; }
    }

    public class GroupedByIpViewModel
    {
        public string IPAddress { get; set; }
        public int MessageCount { get; set; }
        public DateTime FirstMessage { get; set; }
        public DateTime LastMessage { get; set; }
    }

    public class GroupedByDateViewModel
    {
        public DateTime Date { get; set; }
        public int MessageCount { get; set; }
    }
}
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.RazorPages;
using Microsoft.EntityFrameworkCore;
using MessengerApp.Data;
using MessengerApp.Models;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Identity;

namespace MessengerApp.Pages
{
    public class IndexModel : PageModel
    {
        private readonly ApplicationDbContext _context;
        private readonly UserManager<User> _userManager;
        private readonly SignInManager<User> _signInManager; // Добавьте эту строку

        public IndexModel(
            ApplicationDbContext context,
            UserManager<User> userManager,
            SignInManager<User> signInManager) // Добавьте этот параметр
        {
            _context = context;
            _userManager = userManager;
            _signInManager = signInManager; // Инициализируйте
        }

        // Инициализируем свойство, чтобы избежать null
        public List<UserViewModel> Users { get; set; } = new List<UserViewModel>();

        public string CurrentUserId { get; set; } = string.Empty;

        public class UserViewModel
        {
            public string Id { get; set; } = string.Empty;
            public string FirstName { get; set; } = string.Empty;
            public string LastName { get; set; } = string.Empty;
            public string Email { get; set; } = string.Empty;
            public string LastActive { get; set; } = string.Empty;
        }

        public async Task<IActionResult> OnGetAsync()
        {
            // Проверяем, авторизован ли пользователь
            if (!User.Identity.IsAuthenticated)
            {
                // Если не авторизован, перенаправляем на страницу входа
                return RedirectToPage("/Account/Login");
            }

            var currentUser = await _userManager.GetUserAsync(User);
            if (currentUser == null)
            {
                // Если пользователь не найден, разлогиниваем - используем SignInManager
                await _signInManager.SignOutAsync(); // Исправлено здесь
                return RedirectToPage("/Account/Login");
            }

            CurrentUserId = currentUser.Id;

            try
            {
                // Получаем всех пользователей, кроме текущего
                Users = await _context.Users
                    .Where(u => u.Id != currentUser.Id)
                    .OrderBy(u => u.FirstName)
                    .Select(u => new UserViewModel
                    {
                        Id = u.Id,
                        FirstName = u.FirstName ?? string.Empty,
                        LastName = u.LastName ?? string.Empty,
                        Email = u.Email ?? string.Empty,
                        LastActive = u.LastLoginAt.HasValue
                            ? u.LastLoginAt.Value.ToString("g")
                            : "Never"
                    })
                    .ToListAsync();

                // Логируем для отладки
                System.Diagnostics.Debug.WriteLine($"Loaded {Users.Count} users");
            }
            catch (System.Exception ex)
            {
                // В случае ошибки логируем и устанавливаем пустой список
                System.Diagnostics.Debug.WriteLine($"Error loading users: {ex.Message}");
                Users = new List<UserViewModel>();
            }

            return Page();
        }
    }
}
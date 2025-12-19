using Microsoft.AspNetCore.Identity;
using Microsoft.EntityFrameworkCore;
using MessengerApp.Data;
using MessengerApp.Models;
using Microsoft.AspNetCore.Authentication.Cookies;
using Microsoft.AspNetCore.Authentication.Google;
using Microsoft.AspNetCore.Authentication.Facebook;
using Microsoft.AspNetCore.Authentication.MicrosoftAccount;
using MessengerApp.Configuration;

var builder = WebApplication.CreateBuilder(args);

// Конфигурация
builder.Services.Configure<AppSettings>(builder.Configuration.GetSection("AppSettings"));
builder.Services.Configure<JwtSettings>(builder.Configuration.GetSection("JwtSettings"));

// База данных
builder.Services.AddDbContext<ApplicationDbContext>(options =>
    options.UseSqlServer(builder.Configuration.GetConnectionString("DefaultConnection")));

// Identity (сам добавляет Identity.Application схему)
builder.Services.AddIdentity<User, IdentityRole>(options =>
{
    options.Password.RequireDigit = false;
    options.Password.RequiredLength = 1;
    options.Password.RequireNonAlphanumeric = false;
    options.Password.RequireUppercase = false;
    options.Password.RequireLowercase = false;
    options.User.RequireUniqueEmail = true;
    options.SignIn.RequireConfirmedEmail = false;
})
.AddEntityFrameworkStores<ApplicationDbContext>()
.AddDefaultTokenProviders();

// НЕ добавляйте .AddCookie для Identity схем - они уже добавлены через AddIdentity()

// Добавляем внешние провайдеры аутентификации (опционально)
builder.Services.AddAuthentication()
    .AddGoogle(options =>
    {
        var googleSection = builder.Configuration.GetSection("OAuth:Google");
        if (googleSection.Exists() && !string.IsNullOrEmpty(googleSection["ClientId"]))
        {
            options.ClientId = googleSection["ClientId"];
            options.ClientSecret = googleSection["ClientSecret"];
            options.CallbackPath = "/signin-google";
        }
        else
        {
            // Для разработки - можно оставить пустым или использовать тестовые
            Console.WriteLine("Google OAuth not configured");
        }
    });

// Настройка cookie для Identity (уже есть по умолчанию, но можно настроить)
builder.Services.ConfigureApplicationCookie(options =>
{
    options.LoginPath = "/Account/Login";
    options.LogoutPath = "/Account/Logout";
    options.AccessDeniedPath = "/Account/AccessDenied";
    options.ExpireTimeSpan = TimeSpan.FromDays(30);
    options.SlidingExpiration = true;
});

// Сессии
builder.Services.AddSession(options =>
{
    options.IdleTimeout = TimeSpan.FromMinutes(30);
    options.Cookie.HttpOnly = true;
    options.Cookie.IsEssential = true;
    options.Cookie.Name = ".Messenger.Session";
});

builder.Services.AddRazorPages();
builder.Services.AddControllers();

var app = builder.Build();

// Миграция базы данных
using (var scope = app.Services.CreateScope())
{
    var dbContext = scope.ServiceProvider.GetRequiredService<ApplicationDbContext>();
    dbContext.Database.Migrate();

    // Создаем админа при запуске
    var userManager = scope.ServiceProvider.GetRequiredService<UserManager<User>>();
    var roleManager = scope.ServiceProvider.GetRequiredService<RoleManager<IdentityRole>>();

    // Создаем роль Admin если ее нет
    if (!await roleManager.RoleExistsAsync("Admin"))
    {
        await roleManager.CreateAsync(new IdentityRole("Admin"));
        Console.WriteLine("Admin role created");
    }

    // Создаем админа если его нет
    var adminEmail = "admin@example.com";
    var adminUser = await userManager.FindByEmailAsync(adminEmail);
    if (adminUser == null)
    {
        adminUser = new User
        {
            UserName = adminEmail,
            Email = adminEmail,
            FirstName = "Admin",
            LastName = "User",
            EmailConfirmed = true
        };

        var result = await userManager.CreateAsync(adminUser, "Admin123!");
        if (result.Succeeded)
        {
            await userManager.AddToRoleAsync(adminUser, "Admin");
            Console.WriteLine($"Admin user created: {adminEmail} / Admin123!");
        }
    }
}

if (!app.Environment.IsDevelopment())
{
    app.UseExceptionHandler("/Error");
    app.UseHsts();
}
else
{
    app.UseDeveloperExceptionPage();
}

app.UseHttpsRedirection();
app.UseStaticFiles();

app.UseRouting();

// Правильный порядок middleware
app.UseAuthentication();
app.UseAuthorization();
app.UseSession();

app.MapRazorPages();
app.MapControllers();

app.Run();
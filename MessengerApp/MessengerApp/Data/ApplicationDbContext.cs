using Microsoft.EntityFrameworkCore;
using MessengerApp.Models;
using Microsoft.AspNetCore.Identity.EntityFrameworkCore;

namespace MessengerApp.Data
{
    public class ApplicationDbContext : IdentityDbContext<User>
    {
        public ApplicationDbContext(DbContextOptions<ApplicationDbContext> options)
            : base(options)
        {
        }

        public DbSet<Message> Messages { get; set; }
        public DbSet<UserConnection> UserConnections { get; set; }

        protected override void OnModelCreating(ModelBuilder modelBuilder)
        {
            base.OnModelCreating(modelBuilder);

            // Конфигурация для Message
            modelBuilder.Entity<Message>()
                .HasOne(m => m.Sender)
                .WithMany(u => u.SentMessages)
                .HasForeignKey(m => m.SenderId)
                .OnDelete(DeleteBehavior.Restrict);

            modelBuilder.Entity<Message>()
                .HasOne(m => m.Receiver)
                .WithMany(u => u.ReceivedMessages)
                .HasForeignKey(m => m.ReceiverId)
                .OnDelete(DeleteBehavior.Restrict);

            // Индексы для оптимизации запросов
            modelBuilder.Entity<Message>()
                .HasIndex(m => m.SentAt);

            modelBuilder.Entity<Message>()
                .HasIndex(m => m.SenderIP);

            modelBuilder.Entity<UserConnection>()
                .HasIndex(uc => uc.ConnectedAt);
        }
    }
}
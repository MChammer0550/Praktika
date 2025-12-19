using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace MessengerApp.Models
{
    public class UserConnection
    {
        [Key]
        public int Id { get; set; }

        [Required]
        public string UserId { get; set; }

        [Required]
        [MaxLength(45)]
        public string IPAddress { get; set; }

        public DateTime ConnectedAt { get; set; } = DateTime.UtcNow;
        public DateTime? DisconnectedAt { get; set; }

        [ForeignKey("UserId")]
        public virtual User User { get; set; }
    }
}
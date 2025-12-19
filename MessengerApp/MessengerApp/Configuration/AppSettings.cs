namespace MessengerApp.Configuration
{
    public class AppSettings
    {
        public string LogDirectory { get; set; } = "Logs";
        public string LogFileMask { get; set; } = "messenger-*.log";
        public int MaxFileSizeMB { get; set; } = 10;
        public int RetentionDays { get; set; } = 30;
        public string[] AllowedFileTypes { get; set; } = new[] { ".txt", ".jpg", ".png", ".pdf" };
        public long MaxFileSizeBytes { get; set; } = 5242880; // 5MB
    }
}
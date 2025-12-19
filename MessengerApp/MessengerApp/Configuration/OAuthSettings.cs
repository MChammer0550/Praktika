namespace MessengerApp.Configuration
{
    public class OAuthSettings
    {
        public OAuthProvider Google { get; set; }
        public OAuthProvider Facebook { get; set; }
        public OAuthProvider Microsoft { get; set; }
    }

    public class OAuthProvider
    {
        public string ClientId { get; set; }
        public string ClientSecret { get; set; }
    }
}
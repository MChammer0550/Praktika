using System;
using System.ComponentModel.DataAnnotations;

namespace MessengerApp.ViewModels
{
    public class LogFilterViewModel
    {
        [Display(Name = "Start Date")]
        [DataType(DataType.Date)]
        public DateTime? StartDate { get; set; }

        [Display(Name = "End Date")]
        [DataType(DataType.Date)]
        public DateTime? EndDate { get; set; }

        [Display(Name = "IP Address")]
        public string IpAddress { get; set; }

        [Display(Name = "Group by IP")]
        public bool GroupByIp { get; set; }

        [Display(Name = "Group by Date")]
        public bool GroupByDate { get; set; }

        public string SortBy { get; set; } = "Date";
        public string SortOrder { get; set; } = "Desc";
    }
}
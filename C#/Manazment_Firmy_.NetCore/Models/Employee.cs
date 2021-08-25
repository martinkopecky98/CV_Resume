using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.EntityFrameworkCore;
using System.ComponentModel;
using System.ComponentModel.DataAnnotations;

namespace ManazmentFirmy.Models
{
    public class Employee
    {

        [Key]
        public int EmployeeID { get; set; }

        [Required]
        [Display(Name = "Name")]
        public string Name { get; set; }

        [Required]
        [Display(Name = "Surname")]
        public string Surname { get; set; }

        [Required]
        [Display(Name = "Date of Birth")]
        public DateTime BirthDate { get; set; }

        [Required]
        [Display(Name = "Ip address")]
        public string IPaddress { get; set; }


        [Required]
        [Display(Name = "Country")]
        public string IPcountryCode { get; set; }

        [Required]

        public int PositionID { get; set; }

    }
}

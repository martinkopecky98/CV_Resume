using ManazmentFirmy.Models;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;

namespace ManazmentFirmy.DataAccess
{
    public class Databaza : DbContext
    {
        public Databaza(DbContextOptions<Databaza> options) : base(options) { }

        public DbSet<Employee> Employee { get; set; }
        public DbSet<Position> Position { get; set; }
    }
}

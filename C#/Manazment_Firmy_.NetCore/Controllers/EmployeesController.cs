using ManazmentFirmy.DataAccess;
using ManazmentFirmy.Models;
using Microsoft.AspNetCore.Http;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Mvc.Rendering;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using Microsoft.Extensions.Logging;
using System.Net.Http;
using Newtonsoft.Json;
using System.Net;
using System.Text.Json;

namespace ManazmentFirmy.Controllers
{
    public class EmployeesController : Controller
    {
        // GET: EmployeesController

        private readonly Databaza _db;
        public EmployeesController(Databaza db) { _db = db; }
        public ActionResult Index()
        {
            List<Employee> employees = _db.Employee.OrderBy(x => x.PositionID).ToList();
            List<Position> positions = _db.Position.ToList();
            ViewBag.PositionList = positions;
            return View(employees);
        }

        // GET: EmployeesController/Details/5
        public ActionResult Details(int id)
        {
            Employee employee = _db.Employee.Find(id);
            return PartialView("Details", employee);
        }

        // GET: EmployeesController/Create
        public ActionResult Create()
        {
            List<Position> listItems =_db.Position.ToList();
            ViewBag.positionNameList = listItems;
            ViewData["positionNameList"] = listItems;
            return View();
        }

        //private async Task<GeoInfo> getGeoLoc(string ip)
        private async Task<HttpResponseMessage> getGeoLoc(string ip)
        {
            var _httpClient = new HttpClient();
            var response = await _httpClient.GetAsync($"http://api.ipstack.com/{ip}?access_key=a2bff10a43150deddaf5466d79c9da66");
            return response;
        }

        private string getGeoLocFromJson(string json)
        {   
            var listJson = json.Split(",");
            var pom = listJson[4];
            string output = $"{pom[16]}{pom[17]}";
            return output;
        }
        // POST: EmployeesController/Create
        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Create(IFormCollection collection)
        {


            if (ModelState.IsValid)
            {
                 //bacha moze vyvolat SQL injection 
                List<Position> position = _db.Position.FromSqlRaw($"Select * from Position where PositionName = '{collection["PositionID"]}' ").ToList();

                var ip = collection["IPaddress"];
                var json = new WebClient().DownloadString($"http://api.ipstack.com/{ip}?access_key=a2bff10a43150deddaf5466d79c9da66");
       
                Employee employee = new Employee();
                employee.Name = collection["Name"];
                employee.Surname = collection["Surname"];
                employee.BirthDate = Convert.ToDateTime(collection["BirthDate"]);
                employee.IPaddress = collection["IPaddress"];
                employee.IPcountryCode = getGeoLocFromJson(json);
                employee.PositionID = position[0].PositionId;
                _db.Employee.Add(employee);
                _db.SaveChanges();
            }
            return RedirectToAction("Index");
        }

        // GET: EmployeesController/Edit/5
        public ActionResult Edit(int id)
        {
            var obj = _db.Employee.Find(id);
            if (obj == null)
            { return NotFound(); }
            List<Position> positions = _db.Position.ToList();
            ViewBag.positionNameList = positions;

            return View(obj);
        }

        // POST: EmployeesController/Edit/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Edit(int id, IFormCollection collection)
        {
            if (ModelState.IsValid)
            {
                List<Position> position = _db.Position.FromSqlRaw($"Select * from Position where PositionName = '{collection["PositionID"]}' ").ToList();
                Employee employee = _db.Employee.Find(id);

                employee.Name = collection["Name"];
                employee.Surname = collection["Surname"];
                employee.BirthDate = Convert.ToDateTime(collection["BirthDate"]);
                employee.PositionID = position[0].PositionId;
                
                _db.Employee.Update(employee);
                _db.SaveChanges();
            }
            return RedirectToAction("Index");
        }

            // GET: EmployeesController/Delete/5
            public ActionResult Delete(int id)
        {
            var obj = _db.Employee.Find(id);
            if(obj == null)
            { return NotFound(); }

            _db.Employee.Remove(obj);
            _db.SaveChanges();
            return RedirectToAction("Index");
        }

        // POST: EmployeesController/Delete/5
        [HttpPost]
        [ValidateAntiForgeryToken]
        public ActionResult Delete(int id, IFormCollection collection)
        {
            try
            {
                return RedirectToAction(nameof(Index));
            }
            catch
            {
                return View();
            }
        }
    }
}

using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Threading.Tasks;

namespace ManazmentFirmy
{
    //public class GeoHelper
    //{
    //    private readonly IHttpContextAccessor _httpContextAccessor;
    //    private readonly ILogger<GeoHelper> _logger;
    //    private readonly HttpClient _httpClient;

    //    public GeoHelper(IHttpContextAccessor httpContextAccessor)
    //    //public GeoHelper(IHttpContextAccessor httpContextAccessor, ILogger<GeoHelper> logger)
    //    {
    //        _httpContextAccessor = httpContextAccessor;
    //        //_logger = logger;
    //        _httpClient = new HttpClient()
    //        {
    //            Timeout = TimeSpan.FromSeconds(5)
    //        };
    //    }

    //    public async Task<GeoInfo> GetGeoInfo()
    //    {
    //        var ip = _httpContextAccessor.HttpContext.Connection.RemoteIpAddress;

    //        try
    //        {
    //            var response = await _httpClient.GetAsync($"http://freegeoip.net/json/{ip}");

    //            if (response.IsSuccessStatusCode)
    //            {
    //                var json = await response.Content.ReadAsStringAsync();

    //                return JsonConvert.DeserializeObject<GeoInfo>(json);
    //            }
    //        }
    //        catch (Exception ex)
    //        {
    //            //_logger.LogError(ex, "Failed to retrieve geo info for ip '{0}'", ip);
    //        }

    //        return null;
    //    }
    //}


    public class GeoInfoProvider
    {
        private readonly HttpClient _httpClient;
        //create constructor and call HttpClient
        public GeoInfoProvider()
        {
            _httpClient = new HttpClient()
            {
                Timeout = TimeSpan.FromSeconds(5)
            };
        }
        private async Task<string> GetIPAddress()
        {
            var ipAddress = await _httpClient.GetAsync($"http://ipinfo.io/ip");
            if (ipAddress.IsSuccessStatusCode)
            {
                var json = await ipAddress.Content.ReadAsStringAsync();
                return json.ToString();
            }
            return "";
        }
        public async Task<string> GetGeoInfo()
        {
            //I have already created this function under GeoInfoProvider class.
            var ipAddress = await GetIPAddress();
            // When geting ipaddress, call this function and pass ipaddress as given below
            var response = await _httpClient.GetAsync($"http://api.ipstack.com/" + ipAddress + "?access_key=<your key>");
            if (response.IsSuccessStatusCode)
            {
                var json = await response.Content.ReadAsStringAsync();
                var model = new GeoInfo();
                model = JsonConvert.DeserializeObject<GeoInfo>(json);
            }
            return null;
        }
    }
}

using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using System.Globalization;
using Newtonsoft.Json;
using Newtonsoft.Json.Converters;

namespace ManazmentFirmy
{
        public partial class Welcome
        {
            [JsonProperty("greeting")]
            public string Greeting { get; set; }

            [JsonProperty("instructions")]
            public List<string> Instructions { get; set; }
        }

        public partial class Welcome
        {
            public static Welcome FromJson(string json) => JsonConvert.DeserializeObject<Welcome>(json, ManazmentFirmy.Converter.Settings);
        }

        public static class Serialize
        {
            public static string ToJson(this Welcome self) => JsonConvert.SerializeObject(self, ManazmentFirmy.Converter.Settings);
        }

        internal static class Converter
        {
            public static readonly JsonSerializerSettings Settings = new JsonSerializerSettings
            {
                MetadataPropertyHandling = MetadataPropertyHandling.Ignore,
                DateParseHandling = DateParseHandling.None,
                Converters =
            {
                new IsoDateTimeConverter { DateTimeStyles = DateTimeStyles.AssumeUniversal }
            },
            };
        }
}

#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re
import sys
import csv
import os
import json
from datetime import datetime

if len(sys.argv) > 1:
    datestring = sys.argv[1]
else:
    datestring = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

try:
    r = requests.get('http://www.pegelonline.wsv.de/webservices/rest-api/v2/stations.json?includeTimeseries=true&includeCurrentMeasurement=true', timeout=30)
except Exception, e:
    print "Timeout"
    sys.exit()
    
if r.status_code != 200:
    print "Server down"
    sys.exit()

output_path = os.path.join("_scraped_data", datestring)

if not os.path.exists(output_path):
    os.makedirs(output_path)

output_file = open(os.path.join(output_path, "pegelonline.csv"), "wb")
csv_writer = csv.writer(output_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

csv_writer.writerow([
    "Fluss",
    "Zeitpunkt",
    "Station",
    "Meldestufe",
    "latitude",
    "longitude",
    "Wasserstand",
])

for station in r.json():
    station_name = station["longname"]
    fluss = station["water"]["longname"]
    latitude = station["latitude"] if "latitude" in station else ""
    longitude = station["longitude"]  if "longitude" in station else ""
    meldestufe = "-"
    wasserstand = ""
    zeitpunkt = ""
    if len(station["timeseries"]):
        if "currentMeasurement" in station["timeseries"][0]:
            zeitpunkt = station["timeseries"][0]["currentMeasurement"]["timestamp"]
            wasserstand = station["timeseries"][0]["currentMeasurement"]["value"]
            if "stateMnwMhw" in station["timeseries"][0]["currentMeasurement"] and station["timeseries"][0]["currentMeasurement"]["stateMnwMhw"] == "high":
                meldestufe = "Wasserstand oberhalb/gleich mittlerem Höchstwert"
        
    csv_writer.writerow([
        fluss.encode("UTF-8"),
        zeitpunkt.encode("UTF-8"),
        station_name.encode("UTF-8"),
        meldestufe,
        latitude,
        longitude,
        wasserstand
    ])

output_file.close()
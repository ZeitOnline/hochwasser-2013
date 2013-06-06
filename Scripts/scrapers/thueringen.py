#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re
import sys
import csv
import os
from datetime import datetime

if len(sys.argv) > 1:
    datestring = sys.argv[1]
else:
    datestring = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

try:
    r = requests.get('http://www.tlug-jena.de/hw/', timeout=30)
except Exception, e:
    print "Timeout"
    sys.exit()
    
if r.status_code != 200:
    print "Server down"
    sys.exit()

output_path = os.path.join("_scraped_data", datestring)

if not os.path.exists(output_path):
    os.makedirs(output_path)

output_file = open(os.path.join(output_path, "thueringen.csv"), "wb")
csv_writer = csv.writer(output_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

csv_writer.writerow([
    "Fluss",
    "Station",
    "Meldestufe"
])

soup = BeautifulSoup(r.text, "lxml")

rows = soup.select("div.content > div tr")

for i, row in enumerate(rows):

    links = row.select('a[href$=".0_w.html"]')
    for link in links:
        station_name, fluss_name = link.text.split("/")
    
        meldestufe = i+1
    
        csv_writer.writerow([
            fluss_name.encode("UTF-8"),
            station_name.encode("UTF-8"),
            meldestufe
        ])

output_file.close()
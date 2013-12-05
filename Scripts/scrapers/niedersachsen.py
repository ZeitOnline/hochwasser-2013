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
    r = requests.get('http://www.pegelonline.nlwkn.niedersachsen.de/Messwerte', timeout=30)
except Exception, e:
    print "Timeout"
    sys.exit()
    
if r.status_code != 200:
    print "Server down"
    sys.exit()

output_path = os.path.join("_scraped_data", datestring)

if not os.path.exists(output_path):
    os.makedirs(output_path)

output_file = open(os.path.join(output_path, "niedersachsen.csv"), "wb")
csv_writer = csv.writer(output_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

csv_writer.writerow([
    "Fluss",
    "Station",
    "Zeitpunkt",
    "Wasserstand",
    "Differenz",
    "Meldestufe"
])

soup = BeautifulSoup(r.text, "lxml")

rows = soup.select("tr")

for row in rows:
    tds = row.select("td")
    if len(tds) == 0:
        continue
    fluss_name = tds[1].text.strip()
    station_name = tds[0].text.strip()
    zeitpunkt = tds[2].text.strip()
    wasserstand = tds[3].text.strip()
    differenz = tds[5].text.strip()
    meldestufe = tds[7].text.strip()
    
    csv_writer.writerow([
        fluss_name.encode("UTF-8"),
        station_name.encode("UTF-8"),
        zeitpunkt.encode("UTF-8"),
        wasserstand.encode("UTF-8"),
        differenz.encode("UTF-8"),
        meldestufe.encode("UTF-8")
    ])

output_file.close()
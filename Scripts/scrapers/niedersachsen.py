#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re
import sys
import csv
import os

try:
    r = requests.get('http://www.pegelonline.nlwkn.niedersachsen.de/Messwerte', timeout=30)
except Exception, e:
    print "Timeout"
    sys.exit()
    
if r.status_code != 200:
    print "Server down"
    sys.exit()

if not os.path.exists("_scraped_data"):
    os.makedirs("_scraped_data")

output_file = open("_scraped_data/niedersachsen.csv", "wb")
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
    fluss_name = tds[1].text
    station_name = tds[0].text
    zeitpunkt = tds[2].text
    wasserstand = tds[3].text
    differenz = tds[5].text
    meldestufe = tds[7].text
    
    csv_writer.writerow([
        fluss_name.encode("UTF-8"),
        station_name.encode("UTF-8"),
        zeitpunkt.encode("UTF-8"),
        wasserstand.encode("UTF-8"),
        differenz.encode("UTF-8"),
        meldestufe.encode("UTF-8")
    ])

output_file.close()
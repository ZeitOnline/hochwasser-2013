#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re
import sys
import csv
import os

try:
    r = requests.get('http://www.umwelt.sachsen.de/de/wu/umwelt/lfug/lfug-internet/hwz/inhalt_re.html', timeout=30)
except Exception, e:
    print "Timeout"
    sys.exit()
    
soup = BeautifulSoup(r.text, "lxml")

if r.status_code != 200:
    print "Server down"
    sys.exit()

if not os.path.exists("_scraped_data"):
    os.makedirs("_scraped_data")

output_file = open("_scraped_data/sachsen.csv", "wb")
csv_writer = csv.writer(output_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

links = soup.select('div > a[href^="MP/"]')

csv_writer.writerow([
    "Fluss",
    "Station",
    "Zeitpunkt",
    "Wasserstand",
    "Meldestufe"
])

for link in links:
    content = link["onmouseover"].replace("pegelein(", "").replace(")", "").split(",")
    fluss_name = content[1].strip("'")
    station_name = content[0].strip("'")
    zeitpunkt = content[2].strip("'")
    wasserstand = content[3].strip("'")
    durchfluss = content[4].strip("'")
    meldestufe = "-"
    img = link.select("img")
    if img:
        img = img[0]
        if "as4.gif" in img["src"]:
            meldestufe = "4"
        if "as3.gif" in img["src"]:
            meldestufe = "3"
        if "as2.gif" in img["src"]:
            meldestufe = "2"
        if "as1.gif" in img["src"]:
            meldestufe = "1"
  
    csv_writer.writerow([
        fluss_name.encode("UTF-8"),
        station_name.encode("UTF-8"),
        zeitpunkt.encode("UTF-8"),
        wasserstand.encode("UTF-8"),
        meldestufe.encode("UTF-8")
    ])
        
output_file.close()
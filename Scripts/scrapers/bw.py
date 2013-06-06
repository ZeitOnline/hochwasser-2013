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
    r = requests.get('http://www2.lubw.baden-wuerttemberg.de/public/hvz/overview.html', timeout=30)
except Exception, e:
    print "Timeout"
    sys.exit()
    
if r.status_code != 200:
    print "Server down"
    sys.exit()

output_path = os.path.join("_scraped_data", datestring)

if not os.path.exists(output_path):
    os.makedirs(output_path)

output_file = open(os.path.join(output_path, "bw.csv"), "wb")
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
#soup = BeautifulSoup(open("hessen.html"), "lxml")

rows = soup.select("#HVZListData table tbody tr")

for row in rows:
    tds = row.select("td")
    
    station_name, fluss_name = tds[2].text.split(" / ")
    zeitpunkt = tds[6].text
    wasserstand = tds[3].text
    differenz = tds[4].text
    meldestufe = "-"
    
    img = tds[7].select("img")
    if img:
        img = img[0]
        if "peg_i_5.gif" in img["src"]:
            meldestufe = "zuletzt abgerufener Messwert ≥ 100-jährliches Hochwasser"
        if "peg_i_4.gif" in img["src"]:
            meldestufe = "zuletzt abgerufener Messwert ≥ 50-jährliches Hochwasser"
        if "peg_i_3.gif" in img["src"]:
            meldestufe = "zuletzt abgerufener Messwert ≥ 20-jährliches Hochwasser"
        if "peg_i_2.gif" in img["src"]:
            meldestufe = "zuletzt abgerufener Messwert ≥ 10-jährliches Hochwasser"
        if "peg_i_1.gif" in img["src"]:
            meldestufe = "zuletzt abgerufener Messwert ≥ 2-jährliches Hochwasser"
        if "peg_i_6.gif" in img["src"]:
            meldestufe = "zuletzt abgerufener Messwert < 2-jährliches Hochwasser"
        if "peg_i_7.gif" in img["src"]:
            meldestufe = "zuletzt abgerufener Messwert < Mittelwasser"
        if "peg_i_8.gif" in img["src"]:
            meldestufe = "zuletzt abgerufener Messwert < Niedrigwasser"
        if "peg_i_old.gif" in img["src"]:
            meldestufe = "zuletzt abgerufener Messwert ausserhalb des Zeitlimit"
        
    csv_writer.writerow([
        fluss_name.encode("UTF-8"),
        station_name.encode("UTF-8"),
        zeitpunkt.encode("UTF-8"),
        wasserstand.encode("UTF-8"),
        differenz.encode("UTF-8"),
        meldestufe
    ])

output_file.close()
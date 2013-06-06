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
    r = requests.get('http://luadb.it.nrw.de/LUA/hygon/pegel.php?karte=nrw', timeout=30)
except Exception, e:
    print "Timeout"
    sys.exit()
    
if r.status_code != 200:
    print "Server down"
    sys.exit()

output_path = os.path.join("_scraped_data", datestring)

if not os.path.exists(output_path):
    os.makedirs(output_path)

output_file = open(os.path.join(output_path, "nrw.csv"), "wb")
csv_writer = csv.writer(output_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

csv_writer.writerow([
    "Fluss",
    "Station",
    "Zeitpunkt",
    "Wasserstand",
    "Meldestufe"
])

soup = BeautifulSoup(r.text, "lxml")

img_elements = soup.select("#karte_nrw img[onclick]")

stations = {}

for img in img_elements:
    station_id = img["onmouseover"]
    id_results = re.search(r"(?:\(')(.*?)(?:'\))", station_id)
    station_id = id_results.group(1)
    stations[station_id] = {
        "img_src": img["src"]
    }
    
for station_id, station in stations.iteritems():
    tds = soup.select("#%s td" % station_id.replace(" ", "_"))
    if len(tds) == 0:
        continue
    fluss_name = tds[1].text
    station_name = tds[0].text
    zeitpunkt = tds[2].text
    wasserstand = tds[3].text
    
    meldestufe = "-"
    if station["img_src"] == "gelb.png":
        meldestufe = "Informationsstufe 1"
    if station["img_src"] == "orange.png":
        meldestufe = "Informationsstufe 2"
    if station["img_src"] == "rot.png":
        meldestufe = "Informationsstufe 3"
    if station["img_src"] == "weiss.png":
        meldestufe = "inaktiv"
    
    csv_writer.writerow([
        fluss_name.encode("UTF-8"),
        station_name.encode("UTF-8"),
        zeitpunkt.encode("UTF-8"),
        wasserstand.encode("UTF-8"),
        meldestufe.encode("UTF-8")
    ])

output_file.close()
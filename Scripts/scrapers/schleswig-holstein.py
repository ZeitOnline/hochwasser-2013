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

output_path = os.path.join("_scraped_data", datestring)

if not os.path.exists(output_path):
    os.makedirs(output_path)

output_file = open(os.path.join(output_path, "schleswig-holstein.csv"), "wb")
csv_writer = csv.writer(output_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

csv_writer.writerow([
    "Fluss",
    "Station",
    "Zeitpunkt",
    "Wasserstand",
    "Meldestufe"
])

try:
    r = requests.get('http://www.umweltdaten.landsh.de/public/hsi/pegelliste.html', timeout=30)
except Exception, e:
    print "Timeout"
    sys.exit()
    
if r.status_code != 200:
    print "Server down"
    sys.exit()
    
soup = BeautifulSoup(r.text, "lxml")

rows = soup.select("#ListData .TabBodyList")

expression = re.compile("_a([1-4])_", re.IGNORECASE)

for row in rows:
    tds = row.select("td")
    fluss_name = tds[2].text.split(" / ")[-1]
    station_name = tds[2].text.split(" / ")[0]
    zeitpunkt = tds[6].text
    wasserstand = tds[3].text
    meldestufe = "-"
    img = tds[7].select("img")
    if img:
        img = img[0]
        img_src = img["src"].split("_")[-1]
        img_src = img_src.split(".")[0]
        alarm_match = expression.search(img["src"])
        if alarm_match:
            meldestufe = alarm_match.group(1)
        else:
            if img_src == "0":
                meldestufe = "Niedrigwasser (0)"
            if img_src == "1":
                meldestufe = "Mittleres Niedrigwasser (1)"
            if img_src == "2":
                meldestufe = "Mittelwasser (2)"
            if img_src == "3":
                meldestufe = "Mittelwasser (3)"
            if img_src == "4":
                meldestufe = "Mittelwasser (4)"
            if img_src == "5":
                meldestufe = "Mittleres Hochwasser (5)"
            if img_src == "6":
                meldestufe = "Mittleres Hochwasser (6)"
            if img_src == "7":
                meldestufe = "Mittleres Hochwasser (7)"
            if img_src == "8":
                meldestufe = "Höchstes Hochwasser (8)"
            if img_src == "9":
                meldestufe = "Höchstes Hochwasser (9)"

    csv_writer.writerow([
        fluss_name.encode("UTF-8"),
        station_name.encode("UTF-8"),
        zeitpunkt.encode("UTF-8"),
        wasserstand.encode("UTF-8"),
        meldestufe
    ])

output_file.close()
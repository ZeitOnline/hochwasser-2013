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
    r = requests.get('http://www.hochwasservorhersage.sachsen-anhalt.de/wiskiwebpublic/list_W_0.htm', timeout=30)
except Exception, e:
    print "Timeout"
    sys.exit()

if r.status_code != 200:
    print "Server down"
    sys.exit()

output_path = os.path.join("_scraped_data", datestring)

if not os.path.exists(output_path):
    os.makedirs(output_path)

output_file = open(os.path.join(output_path, "sachsen-anhalt.csv"), "wb")
csv_writer = csv.writer(output_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

csv_writer.writerow([
    "Fluss",
    "Station",
    "Zeitpunkt",
    "Wasserstand",
    "Meldestufe"
])

soup = BeautifulSoup(r.text, "lxml")
#soup = BeautifulSoup(open("hessen.html"), "lxml")

rows = soup.select(".parlist_table tr")

for row in rows:
    if row["class"] and ("tr0" in row["class"] or "tr1" in row["class"]):
        tds = row.select("td")
        fluss_name = tds[0].text
        station_name = tds[1].text
        zeitpunkt = tds[3].text
        wasserstand = tds[4].text.replace(" cm", "")
        meldestufe = "-"
        if "title" in tds[5].attrs.keys():
            meldestufe = tds[5]["title"]
        
        csv_writer.writerow([
            fluss_name.encode("UTF-8"),
            station_name.encode("UTF-8"),
            zeitpunkt.encode("UTF-8"),
            wasserstand.encode("UTF-8"),
            meldestufe.encode("UTF-8")
        ])

output_file.close()
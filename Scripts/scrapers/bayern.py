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
    
base_url = 'http://www.hnd.bayern.de/tabellen/'

try:
    r = requests.get("%s%s" % (base_url, "tabelle_pegel.php?zp=0"), timeout=30)
except Exception, e:
    print "Timeout"
    sys.exit()
    
if r.status_code != 200:
    print "Server down"
    sys.exit()

output_path = os.path.join("_scraped_data", datestring)

if not os.path.exists(output_path):
    os.makedirs(output_path)

output_file = open(os.path.join(output_path, "bayern.csv"), "wb")
csv_writer = csv.writer(output_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

csv_writer.writerow([
    "Fluss",
    "Station",
    "Zeitpunkt",
    "Wasserstand",
    "Differenz",
    "Abfluss",
    "Meldestufe"
])

soup = BeautifulSoup(r.text, "lxml")

link_pool = set()

links = soup.select('body > p a[href^="tabelle_pegel.php?"]')

for link in links:
    link_pool.add(link["href"])

for link in link_pool:
    try:
        sub_r = requests.get("%s%s" % (base_url, link), timeout=30)
    except Exception, e:
        print "Timeout"
        continue
        
    sub_soup = BeautifulSoup(sub_r.text, "lxml")

    rows = sub_soup.select("table tr")

    for row in rows:
        tds = row.select("td")
        
        if len(tds) == 0:
            continue
        if row.attrs and "color:#808080" in row.attrs.values():
            continue
        
        fluss_name = tds[1].text
        station_name = tds[0].text
        zeitpunkt = tds[2].text
        wasserstand = tds[3].text
        differenz = tds[4].text
        abfluss = tds[5].text
        meldestufe = tds[6].text
    
        csv_writer.writerow([
            fluss_name.encode("UTF-8"),
            station_name.encode("UTF-8"),
            zeitpunkt.encode("UTF-8"),
            wasserstand.encode("UTF-8"),
            differenz.encode("UTF-8"),
            abfluss.encode("UTF-8"),
            meldestufe.encode("UTF-8")
        ])

output_file.close()
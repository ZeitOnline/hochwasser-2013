#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re
import sys
import csv
import os

try:
    r = requests.get('http://www.luis.brandenburg.de/w/hwmz/lgb/bbviewer.xml', timeout=30)
except Exception, e:
    print "Timeout"
    sys.exit()

if r.status_code != 200:
    print "Server down"
    sys.exit()

r.encoding = "utf-8"

if not os.path.exists("_scraped_data"):
    os.makedirs("_scraped_data")

output_file = open("_scraped_data/brandenburg.csv", "wb")
csv_writer = csv.writer(output_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

csv_writer.writerow([
    "Fluss",
    "Station",
    "Zeitpunkt",
    "Wasserstand",
    "Meldestufe"
])

soup = BeautifulSoup(r.text, "xml")


items = soup.find_all("item")

imgs = set()

for item in items:
    split_title = item.title.text.split("/")
    station_name = split_title[0]
    fluss_name = split_title[-1]
    wasserstand = item.content.Wasserstand.text.replace(" cm", "")
    zeitpunkt = item.content.Messzeitpunkt.text
    meldestufe = "-"
    meldestufe_img = item.iconclr.text
    if meldestufe_img:
        imgs.add(meldestufe_img)
        if "pegel_k_green" in meldestufe_img:
            meldestufe = 0
        if "pegel_yellow" in meldestufe_img:
            meldestufe = 1
        if "pegel_orange" in meldestufe_img:
            meldestufe = 2
        if "pegel_red" in meldestufe_img:
            meldestufe = 3
        if "pegel_purple" in meldestufe_img:
            meldestufe = 4
        if "pegel_k_grey" in meldestufe_img:
            meldestufe = "keine aktuellen Daten"
    
    csv_writer.writerow([
        fluss_name.encode("UTF-8"),
        station_name.encode("UTF-8"),
        zeitpunkt.encode("UTF-8"),
        wasserstand.encode("UTF-8"),
        meldestufe
    ])

output_file.close()
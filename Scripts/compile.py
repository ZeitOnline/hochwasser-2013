#!/usr/bin/python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import re
import sys
import csv
import glob
import os
from datetime import datetime

# try to get to the scraped data files –
# they’re either a command line argument (path to dir)
# or the default
if len(sys.argv) > 1:
    scraper_data_dir = sys.argv[1]
    if not os.path.isdir(scraper_data_dir):
        print "no scraped data dir"
        sys.exit()
    else:
        # we only want the last part, as makeshift timestamp
        scraper_data_dir = scraper_data_dir.split("/")[-1]
else:
    scraper_data_dirs = sorted([d for d in os.listdir("_scraped_data") if os.path.isdir(os.path.join("_scraped_data", d))], reverse=True)

    if not len(scraper_data_dirs):
        print "no scraped data dir"
        sys.exit()

    # equals the time of the data, as well
    scraper_data_dir = scraper_data_dirs[0]

print scraper_data_dir

rows = []
fieldnames = set()
fieldnames.add("Bundesland")
fieldnames.add("Meldestufe Original")

# Meldestufen
meldestufen_map = {}
meldestufen_file = open("_data/meldestufen.csv")
meldestufen_reader = csv.DictReader(meldestufen_file, delimiter=',')
for meldestufe in meldestufen_reader:
    meldestufen_map[meldestufe["Meldestufe"].strip()] = meldestufe["Wert"].strip()
meldestufen_file.close()

for file in glob.glob(os.path.join("_scraped_data", scraper_data_dir, "*.csv")):
    file_handle = open(file)
    csv_reader = csv.DictReader(file_handle, delimiter=';')
    for fieldname in csv_reader.fieldnames:
        fieldnames.add(fieldname)
    
    for i, row in enumerate(csv_reader):
        if os.path.split(file)[-1].split(".")[0].find("pegelonline") >= 0:
            row["Bundesland"] = "-"
        else:
            row["Bundesland"] = os.path.split(file)[-1].split(".")[0]
        if "Meldestufe" in row:
            row["Meldestufe Original"] = row["Meldestufe"].strip()
            if row["Meldestufe"].strip() in meldestufen_map:
                row["Meldestufe"] = meldestufen_map[row["Meldestufe"].strip()]
            else:
                row["Meldestufe"] = ""
            
        rows.append(row)
        
    file_handle.close()

if not os.path.exists(os.path.join("_totals", scraper_data_dir)):
    os.makedirs(os.path.join("_totals", scraper_data_dir))

output_file = open(os.path.join("_totals", scraper_data_dir, "hochwasser.csv"), "wb")
csv_writer = csv.DictWriter(output_file, fieldnames, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
csv_writer.writeheader()
csv_writer.writerows(rows)

output_file.close()
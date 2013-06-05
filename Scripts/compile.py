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

rows = []
fieldnames = set()
fieldnames.add("Bundesland")
fieldnames.add("Meldestufe Original")

datestring = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

if not os.path.exists("alt-%s" % datestring):
    os.makedirs("_scraped_data/alt-%s" % datestring)

if not os.path.exists("_totals"):
    os.makedirs("_totals")

# Meldestufen
meldestufen_map = {}
meldestufen_file = open("_data/meldestufen.csv")
meldestufen_reader = csv.DictReader(meldestufen_file, delimiter=',')
for meldestufe in meldestufen_reader:
    meldestufen_map[meldestufe["Meldestufe"].strip()] = meldestufe["Wert"].strip()
meldestufen_file.close()

for file in glob.glob('_scraped_data/*.csv'):
    file_handle = open(file)
    csv_reader = csv.DictReader(file_handle, delimiter=';')
    for fieldname in csv_reader.fieldnames:
        fieldnames.add(fieldname)
    
    for i, row in enumerate(csv_reader):
        row["Bundesland"] = os.path.split(file)[-1].split(".")[0]
        if "Meldestufe" in row:
            row["Meldestufe Original"] = row["Meldestufe"]
            if row["Meldestufe Original"].strip() in meldestufen_map:
                row["Meldestufe"] = meldestufen_map[row["Meldestufe Original"].strip()]
            else:
                row["Meldestufe"] = ""
            
        rows.append(row)
        
    file_handle.close()
    os.rename(file, "_scraped_data/alt-%s/%s" % (datestring, os.path.split(file)[-1]))

output_file = open("_totals/hochwasser-%s.csv" % datestring, "wb")
csv_writer = csv.DictWriter(output_file, fieldnames, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
csv_writer.writeheader()
csv_writer.writerows(rows)

output_file.close()
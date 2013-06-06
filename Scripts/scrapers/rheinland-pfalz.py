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

base_url = 'http://www.hochwasser-rlp.de'

try:
    r = requests.get(base_url, timeout=30)
except Exception, e:
    print "Timeout"
    sys.exit()
    
if r.status_code != 200:
    print "Server down"
    sys.exit()

output_path = os.path.join("_scraped_data", datestring)

if not os.path.exists(output_path):
    os.makedirs(output_path)

output_file = open(os.path.join(output_path, "rheinland-pfalz.csv"), "wb")
csv_writer = csv.writer(output_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

csv_writer.writerow([
    "Fluss",
    "Station",
    "Zeitpunkt",
    "Wasserstand",
    "Meldestufe"
])

soup = BeautifulSoup(r.text, "lxml")

links = soup.select('.c_t_info a[href^="/karte/uebersicht/flussgebiet/"]')

for link in links:
    print link["href"]
    
    try:
        sub_r = requests.get("%s%s" % (base_url, link["href"].replace("karte", "pegeluebersichten")), timeout=30)
    except Exception, e:
        print "Timeout"
        continue
        
    sub_soup = BeautifulSoup(sub_r.text, "lxml")

    headlines = sub_soup.select("#col3_content h2")

    for headline in headlines:
        station_name = headline.text.replace("Wasserstand am Pegel ", "")
        fluss_name = link.text
    
        next_node = headline
        while True:
            next_node = next_node.next_sibling
            try:
                tag_name = next_node.name
            except AttributeError:
                tag_name = ""
            if tag_name == "div":
                break
    
        strongs = next_node.select(".nebenpegel_bildunterschrift strong")
        zeitpunkt = strongs[0].text
        wasserstand = strongs[1].text.replace(" cm", "")
    
        meldestufe = "-"
        meldestufe_img = next_node.select(".nebenpegel_bildunterschrift img")[0].next_sibling
        if meldestufe_img:
            meldestufe = unicode(meldestufe_img)
    
        csv_writer.writerow([
            fluss_name.encode("UTF-8"),
            station_name.encode("UTF-8"),
            zeitpunkt.encode("UTF-8"),
            wasserstand.encode("UTF-8"),
            meldestufe.encode("UTF-8")
        ])

output_file.close()
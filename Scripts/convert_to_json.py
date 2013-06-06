#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re
import sys
import csv
import glob
import os
import json
import shutil

# try to get to the right data file
data_dirs = sorted([d for d in os.listdir("_totals") if os.path.isdir(os.path.join("_totals", d))], reverse=True)

if not len(data_dirs):
    print "no data dir"
    sys.exit()

# equals the time of the data, as well
data_time = data_dirs[0]
print data_time

data_file_path = os.path.join("_totals", data_dirs[0], "hochwasser.csv")

try:
    with open(data_file_path): pass
except IOError:
    print "hochwasser.csv not found in data dir"

file_handle = open(data_file_path)
rows = csv.DictReader(file_handle, delimiter=';')

filtered_rows = []
for row in rows:
    if int(row["Meldestufe"]) > 0 and len(row["latitude"]) and len(row["longitude"]):
        filtered_rows.append({
            "Meldestufe": int(row["Meldestufe"]),
            "Meldestufe Original": row["Meldestufe"],
            "Station Original": row["Station Original"],
            "Fluss": row["Fluss"],
            "latitude": float(row["latitude"]),
            "longitude": float(row["longitude"])
        })

if not os.path.exists("_json"):
    os.makedirs("_json")
    
output_file = open("_json/current.json", "wb")
output_file.write("var stations = %s" % json.dumps([row for row in filtered_rows], indent=4))
output_file.close()
if not os.path.isfile ("_json/current.json"):
    print "something went wrong with writing the json file _json/current.json"

shutil.copy("_json/current.json", "_json/%s.json" % data_time)
if not os.path.isfile ("_json/%s.json" % data_time):
    print "something went wrong with writing the json file _json/%s.json"  % data_time
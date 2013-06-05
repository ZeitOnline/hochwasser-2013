#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re
import sys
import csv
import glob
import os
import json

file_handle = open(sys.argv[1])
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
    
output_file = open("_json/%s.json" % os.path.split(sys.argv[1])[-1].split(".")[0], "wb")
output_file.write("var stations = %s" % json.dumps([row for row in filtered_rows], indent=4))
output_file.close()
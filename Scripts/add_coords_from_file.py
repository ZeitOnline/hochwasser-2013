#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re
import sys
import csv
import os

# try to get to the right data file –
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

fieldnames = set()
fieldnames.add("latitude")
fieldnames.add("longitude")

coordinates_filter_map = set()
try:
    state_coordinates_file = open("_data/statecoords.txt")
    state_coordinates = csv.DictReader(state_coordinates_file, delimiter='|')
    for state_coordinate in state_coordinates:
        coordinates_filter_map.add("%s,%s" % (state_coordinate["latitude"], state_coordinate["longitude"]))
    state_coordinates_file.close()
    print "%d state coordinates loaded to filter" % len(coordinates_filter_map)
except IOError:                     
    pass

coordinates_map = {}
filtered = 0
try:
    coordinates_file = open("_data/coords.txt")
    coordinates = csv.DictReader(coordinates_file, delimiter='|')
    for coordinate in coordinates:
        if "%s,%s" % (coordinate["latitude"], coordinate["longitude"]) not in coordinates_filter_map:
            coordinates_map[coordinate["name"]] = {
                "latitude": coordinate["latitude"],
                "longitude": coordinate["longitude"]
            }
        else:
            filtered += 1
    coordinates_file.close()
    print "%d coordinates loaded from csv" % len(coordinates_map)
    print "%d coordinates filtered" % filtered
except IOError:                     
    pass

file_handle = open(data_file_path)
rows = csv.DictReader(file_handle, delimiter=';')
for fieldname in rows.fieldnames:
    fieldnames.add(fieldname)

updated_rows = []

for row in rows:
    station_coord_id = "%s, %s, germany" % (row["Station"].strip(), row["Bundesland"].strip())
    if station_coord_id in coordinates_map:
        row["latitude"] = coordinates_map[station_coord_id]["latitude"]
        row["longitude"] = coordinates_map[station_coord_id]["longitude"]
    updated_rows.append(row)   
            
file_handle.close()
os.rename(data_file_path, data_file_path.replace(".csv", ".nongeo.csv"))

output_file = open(data_file_path, "wb")
csv_writer = csv.DictWriter(output_file, fieldnames, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
csv_writer.writeheader()
csv_writer.writerows(updated_rows)

output_file.close()
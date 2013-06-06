#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re
import sys
import csv
import os

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

fieldnames = set()
fieldnames.add("Station Original")

words_to_remove_file = open("_data/words_to_remove.csv")
words_to_remove_reader = csv.reader(words_to_remove_file)

words_to_remove = set()
for word in words_to_remove_reader:
    words_to_remove.add(word[0].decode("utf-8").strip())

remove_regex = []

for word in words_to_remove:
    remove_regex.append(re.escape(word))

remove_regex = ur"(\b|^)(%s)(\W|$)" % "|".join(remove_regex)
pattern = re.compile(remove_regex, re.IGNORECASE|re.UNICODE)

stations_file = open(data_file_path)
rows = csv.DictReader(stations_file, delimiter=';')
for fieldname in rows.fieldnames:
    fieldnames.add(fieldname)


cleaned_rows = set()
updated_rows = []

for row in rows:
    station = row["Station"].decode("utf-8").strip()
    station = station.replace("_", " ")
    station = pattern.sub("", station)
    station = station.strip()
    station = station.strip("-")
    station = station.strip(",")
    station = station.strip()
    
    row["Station Original"] = row["Station"]
    row["Station"] = station.encode("utf-8")
    updated_rows.append(row)
    
    if station != row["Station Original"].decode("utf-8").strip():
        station = "%s, %s, germany" % (station, row["Bundesland"])
        cleaned_rows.add(station.encode("utf-8"))

stations_file.close()
os.rename(data_file_path, data_file_path.replace(".csv", ".raw.csv"))

if not os.path.exists("_temp"):
    os.makedirs("_temp") 
cleaned_stations_file = open("_temp/cleaned_up_station_names.%s.txt" % data_time, "wb")
csv_writer = csv.writer(cleaned_stations_file, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
csv_writer.writerows([row] for row in cleaned_rows)
cleaned_stations_file.close()


output_file = open(data_file_path, "wb")
csv_writer = csv.DictWriter(output_file, fieldnames, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)
csv_writer.writeheader()
csv_writer.writerows(updated_rows)

output_file.close()
#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
import re
import sys
import csv
import os


file_handle = open(sys.argv[1])
rows = csv.DictReader(file_handle, delimiter=';')

output_file = open("_temp/station_names.txt", "wb")
csv_writer = csv.writer(output_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
csv_writer.writerows([[row["Station"].strip(), row["Bundesland"].strip()] for row in rows])
output_file.close()

file_handle.close()

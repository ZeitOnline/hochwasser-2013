#!/bin/sh

NOW=$(date +"%Y-%m-%d-%H-%M-%S")

echo $NOW

python scrapers/bayern.py $NOW
python scrapers/brandenburg.py $NOW
python scrapers/bw.py $NOW
python scrapers/hamburg.py $NOW
python scrapers/hessen.py $NOW
python scrapers/niedersachsen.py $NOW
python scrapers/nrw.py $NOW
python scrapers/rheinland-pfalz.py $NOW
python scrapers/sachsen.py $NOW
python scrapers/schleswig-holstein.py $NOW
python scrapers/thueringen.py $NOW
python scrapers/sachsen-anhalt.py $NOW
python compile.py
python clean_up_station_names.py
python add_coords_from_file.py
python convert_to_json.py
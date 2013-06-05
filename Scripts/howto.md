# How to

1. `./hochwasser.sh` scrapes all the websites
2. `python compile.py` compiles the various resulting csvs into one big list, normalises the *Meldestufen*
3. `python clean_up_station_names.py filename.csv` cleans up all the station names for better geocoding
4. `python add_coords_from_file.py filename.csv` adds gps coords from the file in `_data/coords.txt`
5. `python convert_to_json.py filename.csv` converts the csv to json, filters out stations without gps coords or Meldestufe < 1

# Dependencies

* geopy
* requests
* lxml
* beautifulsoup4


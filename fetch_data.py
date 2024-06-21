import gspread 
import yaml
import csv
import pandas as pd
import os
import json 
from py.helpers import *

results_wkbk_url = "https://docs.google.com/spreadsheets/d/17Wa4KKc8OK_vU8T4SrZxivgjhVL9_PmW30AxQiZH5jM/edit#gid=0"
results_sheet_num = 0 # first sheet
local_creds_path = '/Users/rasikaramanan/Documents/coding_projects/pokerpanther.github.io/google_creds.json'


creds_dict = {}

if os.getenv("GOOGLE_CREDS"): # running from GitHub
    creds_str = os.getenv("GOOGLE_CREDS")
    creds_dict = json.loads(creds_str)
else: # running locally/manually
    creds_dict = json.load(open(local_creds_path))

gc = gspread.service_account_from_dict(creds_dict)
wkbk = gc.open_by_url(results_wkbk_url)
sheet = wkbk.get_worksheet(results_sheet_num) 
data = sheet.get_all_values() # data is a list of lists
orig_col_names = data[0] # first list is col names
col_names = [to_snake_case(s) for s in orig_col_names]
data_dicts = [dict(zip(col_names, row)) for row in data[1:]]
all_results = pd.DataFrame(data_dicts)

all_results['place'] = all_results['place'].apply(convert_place)
all_results['date'] = all_results['date'].apply(convert_date)
for float_col in ['net', 'cash_in', 'cash_out']:
    all_results[float_col] = all_results[float_col].apply(convert_float)
for int_col in ['bullets', 'duration_min']:
    all_results[int_col] = all_results[int_col].apply(convert_int)

online_results = all_results[all_results["type"].str.strip().str.lower() == "online"].copy()
live_results = all_results[all_results["type"].str.strip().str.lower() == "live"].copy()

online_stats = calc_stats(online_results, "Online")
live_stats = calc_stats(live_results, "Live")
overall_stats = calc_stats(all_results, "All")

with open('_data/results.yml', 'w') as file:
    yaml.dump(all_results.to_dict(orient='records'), file, sort_keys=False)
    
with open('_data/col_name_map.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['var_name', 'display_name'])
    for var_name, display_name in zip(col_names, orig_col_names):
        writer.writerow([var_name, display_name])


with open('_data/stats.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(list(online_stats.keys()))
    for stats in [online_stats, live_stats, overall_stats]:
        writer.writerow(list(stats.values()))

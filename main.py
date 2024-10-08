import gspread 
import yaml
import csv
import pandas as pd
import time
import sys
from py.helpers import *

results_wkbk_url = "https://docs.google.com/spreadsheets/d/17Wa4KKc8OK_vU8T4SrZxivgjhVL9_PmW30AxQiZH5jM/edit#gid=0"
results_sheet_num = 0 # first sheet


## Fetch data from Google Drive and store as pandas df ##
sheet = None
for attempt in range(3): # try to fetch the worksheet 3 times
    try:
        creds_dict = get_google_creds()
        gc = gspread.service_account_from_dict(creds_dict)
        wkbk = gc.open_by_url(results_wkbk_url)
        sheet = wkbk.get_worksheet(results_sheet_num) 
        break
    except Exception as e:
        print(f"Attempt {attempt + 1} failed.")
        print(f"Exception type: {type(e).__name__}")  # Print the type of exception
        print(f"Exception message: {str(e)}")  # Print the exception message
        time.sleep(30) # wait 30 secs between attempts

if sheet is None: # if all 3 attempts failed 
    print("Failed to retrieve data after multiple attempts.")
    sys.exit(1)

data = sheet.get_all_values() # data is a list of lists
orig_col_names = data[0] # first list is col names
col_names = [to_snake_case(s) for s in orig_col_names]
data_dicts = [dict(zip(col_names, row)) for row in data[1:]]
all_results = pd.DataFrame(data_dicts)


## Normalize data and write to results.yml and col_name_map.csv

all_results['place'] = all_results['place'].apply(convert_place)
all_results['date'] = all_results['date'].apply(convert_date)
for float_col in ['net', 'cash_in', 'cash_out']:
    all_results[float_col] = all_results[float_col].apply(convert_float)
for int_col in ['bullets', 'duration_min']:
    all_results[int_col] = all_results[int_col].apply(convert_int)

with open('_data/results.yml', 'w') as file:
    yaml.dump(all_results.to_dict(orient='records'), file, sort_keys=False)
    
with open('_data/col_name_map.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['var_name', 'display_name'])
    for var_name, display_name in zip(col_names, orig_col_names):
        writer.writerow([var_name, display_name])


## Calculate aggregate statistics and write to stats.csv ##

online_results = all_results[all_results["type"].str.strip().str.lower() == "online"].copy()
live_results = all_results[all_results["type"].str.strip().str.lower() == "live"].copy()

online_stats = calc_stats(online_results, "Online")
live_stats = calc_stats(live_results, "Live")
overall_stats = calc_stats(all_results, "All")

with open('_data/stats.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(list(online_stats.keys()))
    for stats in [online_stats, live_stats, overall_stats]:
        writer.writerow(list(stats.values()))

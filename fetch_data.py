import gspread 
import yaml
import re
import csv
import pandas as pd
from datetime import datetime

results_wkbk_url = "https://docs.google.com/spreadsheets/d/17Wa4KKc8OK_vU8T4SrZxivgjhVL9_PmW30AxQiZH5jM/edit#gid=0"
results_sheet_num = 0 # first sheet
local_creds_path = '/Users/rasikaramanan/Documents/coding_projects/pokerpanther.github.io/google_creds.json'

def to_snake_case(input_string):
    # Replace spaces with underscores
    snake_case_str = input_string.replace(" ", "_")
    
    # Replace non-alphanumeric characters with underscores
    snake_case_str = "".join(["_" if not c.isalnum() else c for c in snake_case_str])
    
    # Convert to lowercase
    snake_case_str = snake_case_str.lower()
    
    # Remove leading and trailing underscores
    snake_case_str = snake_case_str.strip("_")

    # Replace multiple underscores with a single underscore
    snake_case_str = re.sub(r'_{2,}', '_', snake_case_str)

    return snake_case_str


def calc_stats(df, type): 
    """ takes in a pandas df and a string representing 
    the tournament type; returns a dict with desired stats 
    """

    total_profit = df['net'].sum()
    num_buy_ins = df['bullets'].sum()
    total_cash_in = df['cash_in'].sum()
    total_cash_out = df['cash_out'].sum()
    roi = 100 * ((total_cash_out - total_cash_in) / total_cash_in)
    ave_buy_in =  total_cash_in / num_buy_ins

    stats = {
        "type":         type,
        "total_profit": round(total_profit, 2), 
        "num_buy_ins":  num_buy_ins,
        "roi":          round(roi, 2),
        "ave_buy_in":   round(ave_buy_in, 2)
    }

    return stats

def set_data_types(df):
    # convert numerical cols to number types
    for col in ['net', 'cash_in', 'cash_out']: 
        df[col] = df[col].str.replace('[$,]', '', regex=True).astype(float)
    for col in ['bullets', 'duration_min']:
        df[col] = df[col].astype(int)

def convert_date(date_str):
    date = datetime.strptime(date_str, "%m/%d/%y")
    sortable = date.strftime('%Y-%m-%d')
    display = date.strftime("%-m/%-d/%-y")
    return {'display': display, 'sortable': sortable}

def convert_place(place_str):
    num_match = re.findall(r'\d+', place_str)
    num = 6.022e23 # v big 
    if num_match:
        num = int(num_match[0])
        suffixes = {1: 'st', 2: 'nd', 3: 'rd'}
        if 10 <= num % 100 <= 20:
            suffix = 'th'
        else:
            suffix = suffixes.get(num % 10, 'th')
        place_str = str(num) + suffix         
    return {'display': place_str, 'sortable': num}

gc = gspread.service_account(filename=local_creds_path)
wkbk = gc.open_by_url(results_wkbk_url)
sheet = wkbk.get_worksheet(results_sheet_num) 
data = sheet.get_all_values() # data is a list of lists
orig_col_names = data[0] # first list is col names
col_names = [to_snake_case(s) for s in orig_col_names]
data_dicts = [dict(zip(col_names, row)) for row in data[1:]]
all_results = pd.DataFrame(data_dicts)
set_data_types(all_results)
all_results['place'] = all_results['place'].apply(convert_place)
all_results['date'] = all_results['date'].apply(convert_date)

online_results = all_results[all_results["type"].str.strip().str.lower() == "online"].copy()
live_results = all_results[all_results["type"].str.strip().str.lower() == "live"].copy()

online_stats = calc_stats(online_results, "Online")
live_stats = calc_stats(live_results, "Live")
overall_stats = calc_stats(all_results, "All")


with open('./_data/results.yml', 'w') as file:
    yaml.dump(all_results.to_dict(orient='records'), file, sort_keys=False)

with open('./_data/col_name_map.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['var_name', 'display_name'])
    for var_name, display_name in zip(col_names, orig_col_names):
        writer.writerow([var_name, display_name])


with open('./_data/stats.csv', 'w') as file:
    writer = csv.writer(file)
    writer.writerow(list(online_stats.keys()))
    for stats in [online_stats, live_stats, overall_stats]:
        writer.writerow(list(stats.values()))

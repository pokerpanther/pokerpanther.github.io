import gspread 
import yaml
import re
import csv

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

gc = gspread.service_account(filename=local_creds_path)
wkbk = gc.open_by_url(results_wkbk_url)
sheet = wkbk.get_worksheet(results_sheet_num) 
data = sheet.get_all_values() # data is a list of lists
orig_col_names = data[0] # first list is col names
col_names = [to_snake_case(s) for s in orig_col_names]
data_dicts = [dict(zip(col_names, row)) for row in data[1:]]

with open('./_data/results.yml', 'w') as file:
    yaml.dump(data_dicts, file, sort_keys=False)

with open('./_data/col_name_map.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['var_name', 'display_name'])
    for var_name, display_name in zip(col_names, orig_col_names):
        writer.writerow([var_name, display_name])


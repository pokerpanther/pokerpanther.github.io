import re
from datetime import datetime
import os
import json 

def get_google_creds():
    creds_dict = {}
    local_creds_path = '/Users/rasikaramanan/Documents/coding_projects/pokerpanther.github.io/google_creds.json'
    if os.getenv("GOOGLE_CREDS"): # running from GitHub
        creds_str = os.getenv("GOOGLE_CREDS")
        creds_dict = json.loads(creds_str)
    else: # running locally/manually
        with open(local_creds_path, 'r') as f:
            creds_dict = json.load(f)
    return creds_dict

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

def convert_float(num_str):
    # convert num_str with chars like '$' to float
    try:
        return float(re.sub(r'[^-0-9.]', '', num_str))
    except:
        return num_str

def convert_int(num_str):
    try:
        return int(re.sub(r'[^-0-9]', '', num_str))
    except:
        return num_str

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

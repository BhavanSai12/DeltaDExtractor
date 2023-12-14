import requests
import json
import pandas as pd
import os

def fetch_json_data(url, city_name):
    try:
        # Fetch JSON data from the URL
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        json_data = response.json()

        print(f"Data for {city_name} has been successfully fetched")

        return json_data  # Return the JSON data

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for {city_name}: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred for {city_name}: {req_err}")
    except json.decoder.JSONDecodeError as json_err:
        print(f"JSON decoding error occurred for {city_name}: {json_err}")
    return None  # Return None if an error occurs

# PPO (Product Code)
base_url = "https://www.deltadental.com/conf/ddpa/paths/dentistsearchrest.json?maximumDistance=500&sortType=0&productCode=PPO&maximumNumberOfRecordsToReturn=1000&city="

# Read city names from a text file
file_path = r"C:\Users\Truvisroy Solutions\Desktop\DeltaDentalData Extractions\scripts\city_names.txt"

merged_data = []

with open(file_path, 'r') as file:
    provided_city_names = [line.strip() for line in file]

# Iterate through each city and call the function
for city_name in provided_city_names:
    url = f"{base_url}{city_name}"
    json_data = fetch_json_data(url, city_name)

    if json_data:
        # Assuming 'listOfLocations' is present in each JSON file
        merged_data.extend(json_data.get('listOfLocations', []))

# Create a DataFrame from the merged data
df = pd.DataFrame(merged_data)

# Save the DataFrame to an Excel file
excel_output_path = 'Alabhama.xlsx'       #update here with state name....
print('Completed Data Scrapping!....')
df.to_excel(excel_output_path, index=False)

print(f'Data saved to Excel file: {excel_output_path}')

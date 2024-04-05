from selenium import webdriver
from typing import List
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException


import os
import csv
import json
import path


def make_chrome_headless(o=True):
    """
    Return a headless driver of Chrome
    """
    try:
        options = Options()
        # Obtener la ruta del ejecutable de ChromeDriver utilizando webdriver_manager
        chromedriver_path = ChromeDriverManager().install()
        service = Service(executable_path=chromedriver_path)

        if o:
            # options.add_argument("--headless")
            # options.add_argument("--disable-extensions")
            # options.add_argument("--log-level=3")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920x1080")
            options.add_argument("--disable-extensions")

            options.add_experimental_option(
                "excludeSwitches", ["enable-logging"])
            headless_driver = webdriver.Chrome(
                service=service, options=options)
            # headless_driver = webdriver.Chrome(ChromeDriverManager().install(), options= options)
    except Exception as e:
        print(f"Error: {e}")
        # Handle the exception here (e.g., display an error message or try again)
        headless_driver = None  # Handle the exception gracefully
    return headless_driver


def make_chrome():
    """
    Return a non-headless driver of Chrome
    """
    try:
        driver = webdriver.Chrome(ChromeDriverManager().install())
    except Exception as e:
        print(f"PermissionError: {e}")
        driver = None  # Handle the exception gracefully
    return driver


'''
def check_if_file_exist(file_path):
    # Verificar si el archivo existe
    # Check if the file exists
    if os.path.exists(file_path):
        print(f"The JSON file '{file_path}' already exists.")
    else:
        # Create a new JSON file with some initial Data
        Data = {}
        # Write the Data to the file
        with open(file_path, 'w') as json_file:
            json.dump(Data, json_file)
            print(f"Created a new JSON file '{file_path}' with initial Data.")
    # Now you can work with the JSON file, either existing or newly created.
'''


def check_if_file_exist(file_path, file_type='json'):
    # Check if the file exists
    if os.path.exists(file_path):
        print(f"The {file_type.upper()} file '{file_path}' already exists.")
    else:
        # Create a new file with some initial Data based on the file type
        data = {}
        if file_type == 'json':
            # For JSON files
            with open(file_path, 'w') as json_file:
                json.dump(data, json_file)
            print(f"Created a new JSON file '{file_path}' with initial Data.")
        elif file_type == 'csv':
            # For CSV files
            with open(file_path, 'w', newline='') as csv_file:
                csv_writer = csv.writer(csv_file)
                # Add header if needed
                # csv_writer.writerow(['Column1', 'Column2', ...])
                # Write the Data to the file
                # csv_writer.writerow([value1, value2, ...])
            print(f"Created a new CSV file '{file_path}' with initial Data.")
        else:
            print(f"Unsupported file type: {file_type}")


def fail_message(e):
    """
    Print failure message
    """
    template = "An exception of type {0} occurred. Arguments:\n{1!r}"
    message = template.format(type(e).__name__, e.args)
    print(message)


def save_generic(path, collection):
    if not isinstance(collection, (list, dict, tuple)):
        raise TypeError('Collection is not serializable')
    json_string = json.dumps(collection, ensure_ascii=False, indent=2)
    with open(path, 'w', encoding="utf-8") as outfile:
        outfile.write(json_string)


def load_generic(path):
    with open(path, encoding='utf-8') as fh:
        elements = json.load(fh)
    return elements


def save_list_as_csv(data_list, file_path):
    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(data_list)


def load_csv(path):
    file = open(path, encoding="utf8")
    raw_data = csv.reader(file, delimiter=',', quotechar='"')
    datum = list(raw_data)
    # Data = list(csv.DictReader(file, delimiter=",", quotechar='"'))
    # file.close()
    return datum


def reverse_country_codes():
    path = 'Data/Options/countryCodesList.json'
    data = load_generic(path)

    # Create a dictionary with "code" as the key
    country_dict = {entry["code"]: entry for entry in data}
    # Access the information for a specific country code (e.g., "DZ")
    desired_country_info = country_dict.get("DZ")

    save_generic('Data/country_codes.json', country_dict)


def csv_generics(path, list, cols):
    csv_file = path
    csv_columns = cols
    with open(csv_file, 'w', encoding='utf-8', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for data in list:
            # print(Data)
            writer.writerow(data)


def load_csv_generic(path):
    with open(path, 'r') as file:
        csvreader = csv.reader(file)
        return csvreader


def read_csv(path):
    with open(path, 'r') as file:
        csvreader = csv.reader(file)
        for row in csvreader:
            print(row)


def load_csv(path):
    file = open(path, encoding="utf8")
    raw_data = csv.reader(file, delimiter=',', quotechar='"')
    datum = list(raw_data)
    # Data = list(csv.DictReader(file, delimiter=",", quotechar='"'))
    # file.close()
    return datum


# if __name__ == '__main__':
    # reverse_country_codes()
    # pass

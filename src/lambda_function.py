import logging
import datetime
from bs4 import BeautifulSoup
import requests
"""
Pandas can be imported as a Layer inside of the AWS Lambda function, hence doesn't need to be imported here.
"""
# import pandas as pd
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# variables
advisory_url = "https://travel.gc.ca/travelling/advisories"

# file config
date = "{:%B %d, %Y}".format(datetime.datetime.now())
filename = "data_{date}.csv"
local_path = "/tmp/" + filename


# helper function for adding each country's data to the csv file as program iterates through 'countries' list
def addNewEntry(countries):
    # recursion statement
    if not countries or countries[0] is None:
        return False

    # get all the data we need out of the web element
    country_elements = countries[0].find_all("td")
    #print(f"country_elements: {country_elements}") ---TESTING---
    name = country_elements[1].a.string
    temp = country_elements[2].div
    risk = temp["class"][0]
    description = temp.text.strip()
    updated = country_elements[3].text

    # create a new row of data to be added
    new_row = {"Country": name,
               "Risk Level": risk,
               "Description": description,
               "Last Updated": updated}
    
    # add the row to the DataFrame
    pd.DataFrame([new_row]).to_csv(local_path, mode="a", header=False, index=False)
    #print(f"Added: {new_row}") ---TESTING---

    # recursively run again with the next country in list
    return addNewEntry(countries[1:])

def makeData():
    page = requests.get(advisory_url)
    soup = BeautifulSoup(page.text, "html.parser")

    table = soup.find("tbody")

    first_country = table.find("tr")
    countries = []
    countries.extend([first_country])
    while True:
        try:
            countries.extend([countries[-1].find_next_sibling("tr")])
        except:
            break

    # create an empty dataFrame with only the column names
    df = pd.DataFrame(columns=["Country", "Risk Level", "Description", "Last Updated"])

    # create a csv file for the data
    df.to_csv(local_path, index=False)

    # add data from countries list
    addNewEntry(countries)

def lambda_handler(event, context):
    # scraper process
    logger.info("Starting Scraper.")
    makeData()
    logger.info("Scraper Finished.")

    # upload to s3
    s3 = boto3.client("s3")
    bucket_name = "travel-advisory-bucket"
    s3.upload_file(local_path, bucket_name, f"{date}/{filename}")

    return {
        "statusCode": 200,
        "body": "Data Extracted."
    }


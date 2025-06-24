import logging
from bs4 import BeautifulSoup
import requests
import numpy as np
import pandas as pd

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# variables
advisory_url = "https://travel.gc.ca/travelling/advisories"


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
    description = temp.text
    updated = country_elements[3].text

    # create a new row of data to be added
    new_row = {"Country": name,
               "Risk Level": risk,
               "Description": description,
               "Last Updated": updated}
    
    # add the row to the DataFrame
    pd.DataFrame([new_row]).to_csv("data.csv", mode="a", header=False, index=False)
    print(f"Added: {new_row}")

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
    """
    for country in countries[6:7]:
        elements = country.find_elements(By.TAG_NAME, "td")
        #element_img = elements[0].find_element(By.TAG_NAME, "img")
        element_name = elements[0].find_element(By.TAG_NAME, "a")
        element_desc = elements[1].find_element(By.TAG_NAME, "div")
        element_updated = elements[2]
    print(element_name.text, element_desc.get_attribute("class"), element_desc.text, element_updated.text)
    """

    # create an empty dataFrame with only the column names
    df = pd.DataFrame(columns=["Country", "Risk Level", "Description", "Last Updated"])

    # create a csv file for the data
    df.to_csv("data.csv", index=False)

    # add data from countries list
    addNewEntry(countries)

if __name__ == '__main__':
    makeData()


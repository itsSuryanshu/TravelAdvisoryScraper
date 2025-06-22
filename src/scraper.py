from selenium import webdriver
from selenium.webdriver.common.by import By
import numpy as np
import pandas as pd
import undetected_chromedriver as uc
import os

# variables
advisory_url = "https://travel.gc.ca/travelling/advisories"


# helper function for adding each country's data to the csv file as program iterates through 'countries' list
def addNewEntry(countries):
    # recursion statement
    if not countries:
        return False

    # get all the data we need out of the web element
    country_elements = countries[0].find_elements(By.TAG_NAME, "td")
    name = country_elements[0].find_element(By.TAG_NAME, "a").text
    temp = country_elements[1].find_element(By.TAG_NAME, "div")
    risk = temp.get_attribute("class")
    description = temp.text
    updated = country_elements[2].text

    # create a new row of data to be added
    new_row = {"Country": name,
               "Risk Level": risk,
               "Description": description,
               "Last Updated": updated}
    
    # add the row to the DataFrame
    pd.DataFrame([new_row]).to_csv("data.csv", mode="a", header=False, index=False)

    # recursively run again with the next country in list
    addNewEntry(countries[1:])

def getData():
    browser_options = webdriver.ChromeOptions()
    browser = uc.Chrome(options=browser_options)
    browser.get(advisory_url)

    table = browser.find_element(By.CSS_SELECTOR, "#reportlist")

    countries = []
    n = len(table.find_elements(By.TAG_NAME, "tr"))
    x = 1
    while (x < n):
        countries.extend(table.find_elements(By.CSS_SELECTOR, f"#reportlist > tbody:nth-child(2) > tr:nth-child({x})"))
        x += 1

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

if __name__ == "__main__":
    getData()


'''
Scrap for any item an olx.pl 
1. Go to olx.pl and search the item 
2. Copy the desired URL and enter it after the script

Example: 

python simple_price_scraper_olx.py https://www.olx.pl/elektronika/q-klawiatura-logitech-mx/

This will create a data.csv file with the next columns: item_name, item_link and price.
'''

from bs4 import BeautifulSoup
import requests
import time
import click
#import numpy as np
import pandas as pd
#from datetime import datetime


def offer_download_function(item):

  # creating a list with feature names
  result = [ ["item_name", 
              "item_link", 
              "price"] ]

  # getting the number of available pages in the search result
  base_url = "https://www.olx.pl" 
  offer_url = item
  page_req = requests.get(offer_url)
  html = page_req.content
  soup = BeautifulSoup(html, "html.parser")
  numbers_of_pages = int(soup.find_all("a", {"class": "css-1mi714g"})[-1].text.strip())

  # loop to download all pages
  for n_pages in range(1, numbers_of_pages+1):
    time.sleep(2)
    URL_pages = offer_url + "?page=" + str(n_pages)
    task_page = requests.get(URL_pages) 
    print("Pages:", n_pages, "|", "Status:", task_page, sep=" ", end="\n")

    html_pages = task_page.content

    # creating a BeautifulSoup object
    soup_pages = BeautifulSoup(html_pages, "html.parser")

    # list with information about offers from the parsed website
    offers_list = soup_pages.find_all("div", {"class": "css-1sw7q4x"})
    offers_list = offers_list[:-1]
    print("List of offers on page:", len(offers_list), "| Pages: [", n_pages, "/", numbers_of_pages, "]", sep=" ", end="\n")

    for offer in offers_list:
    
      item_name = offer.find("h6", {"class": "css-16v5mdi er34gjf0"}).text
      
      item_html = offer.find("a").get("href")
      item_link = base_url + item_html
      
      price = offer.find("p", {"class": "css-10b0gli er34gjf0"}).text

      # creating a set of results
      result.append( [item_name, 
                    item_link, 
                    price ] )

  return(pd.DataFrame(result[1:], columns=result[0]))


@click.command()
@click.argument('item')


def main(item):
  data_df = offer_download_function(item)
  data_df.to_csv("data.csv", index=False)


if __name__ == "__main__":

    print("OLX Web Scraper!")
    main()
import csv
import requests
from scraping import get_product_information
from datetime import datetime

scrap_url = 'https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html'

r = requests.get(scrap_url)
status_code = r.status_code

current_date = datetime.now().strftime("%Y%m%d_%H%M%S")

if status_code == 200:
    print('Successfully scraped')
    headers = ['product_page_url','universal_product_code','title','price_including_tax','price_excluding_tax',
               'number_available','product_description','category','review_rating','image_url']
    data = [get_product_information(r.content, scrap_url)]

    # extract to csv
    with open('extract/extract_one_product_'+ current_date +'.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, delimiter=',',fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
else:
    print('Failed to scrape, the product at: ' + str(scrap_url))
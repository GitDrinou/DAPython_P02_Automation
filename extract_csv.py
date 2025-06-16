import csv
import requests
from scraping import get_product_information

scrap_url = 'https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html'

r = requests.get(scrap_url)
status_code = r.status_code

if status_code == 200:
    print('Successfully scraped')
    headers = ['product_page_url','universal_product_code','title','price_including_tax','price_excluding_tax',
               'number_available','product_description','category','review_rating','image_url']
    data = [get_product_information(r.content, scrap_url)]

    # extract to csv
    with open('extract/one_product.csv', 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, delimiter=',',fieldnames=headers)
        writer.writeheader()
        writer.writerows(data)
else:
    print('Failed to scrape, the product at: ' + str(scrap_url))
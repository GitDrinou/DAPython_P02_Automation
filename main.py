import csv
import requests
from bs4 import BeautifulSoup

from scraping import get_product_information
from datetime import datetime

is_category = False
current_date = datetime.now().strftime("%Y%m%d_%H%M%S")

headers = ['product_page_url','universal_product_code','title','price_including_tax','price_excluding_tax',
           'number_available','product_description','category','review_rating','image_url']

scrap_url = 'https://books.toscrape.com/catalogue/category/books/mystery_3/index.html'

for item in scrap_url.split('/'):
    if item == 'category':
        is_category = True
        break

r = requests.get(scrap_url)
status_code = r.status_code

if status_code == 200:
    if is_category:
        print("Category found.")
        soup = BeautifulSoup(r.content, 'html.parser')
        soup.prettify()
        books_url = []
        books = soup.find_all('div', class_='image_container')
        for book in books:
           books_url.append(book.find('a')['href'])
        # print("Found {} books.".format(len(books)))
    else:
        data = [get_product_information(r.content, scrap_url)]

    # extract to csv
    # with open('extract/extract_one_product_'+ current_date +'.csv', 'w', newline='', encoding='utf-8') as file:
    #     writer = csv.DictWriter(file, delimiter=',',fieldnames=headers)
    #     writer.writeheader()
    #     writer.writerows(data)

    print('Successfully scraped')
else:
    print('Failed to scrape, the product at: ' + str(scrap_url))
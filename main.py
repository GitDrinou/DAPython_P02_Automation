from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from csv_writer import write_file
from scraping import get_product_information

is_category = False
books_url = []
data = []
i = 0

# TODO: change to a Prompt user
scrap_url = 'https://books.toscrape.com/catalogue/category/books/mystery_3/'

while scrap_url:
    for item in scrap_url.split('/'):
        if item == 'category':
            is_category = True
            break

    if is_category:
        response = requests.get(scrap_url)
        if response.status_code == 200:

            soup = BeautifulSoup(response.content, 'html.parser')
            soup.prettify()

            books = soup.find_all('div', class_='image_container')
            for book in books:
                books_url.append(book.find('a')['href'].split('../')[-1])

            next_page_btn = soup.find('li', class_='next')

            if next_page_btn:
                url_next = next_page_btn.find('a')['href']
                scrap_url = urljoin(scrap_url, url_next)
            else:
                scrap_url = None
        else:
            scrap_url = None
            print('Failed to scrap the page')

    else:
        response = requests.get(scrap_url)
        status_code = response.status_code

        if status_code == 200:
            data = [get_product_information(response.content, scrap_url)]
            scrap_url = None
        else:
            print('Failed to scrape the page at: ' + scrap_url)
            scrap_url = None

print('Loading...')
for book in books_url:
    url = urljoin('https://books.toscrape.com/catalogue/', book)
    response = requests.get(url)

    print('*', end='', flush=True)
    if response.status_code == 200:
        data.append(get_product_information(response.content, url))
        i += 1
    else:
        print('Failed to scrap the page')


if len(data) > 0:
    write_file(data, is_category)
    print('\nSuccessfully saved the data')
import pandas as pd

from bs4 import BeautifulSoup
from urllib.parse import urljoin
from generate_csv_files import generate_file, generate_all_category_files
from scraping import get_product_information, get_html

is_category = False
is_all_product = False
books_url = []
data = []
i = 0

# TODO: change to a Prompt user
scrapped_url = 'https://books.toscrape.com'
base_product_url = 'https://books.toscrape.com/'

print('Loading...')
while scrapped_url:
    if scrapped_url == 'https://books.toscrape.com':
        is_all_product = True
    else:
        for item in scrapped_url.split('/'):
            if item == 'category':
                is_category = True
                break

    if is_category or is_all_product:

        html = get_html(scrapped_url)
        soup = BeautifulSoup(html, 'html.parser')

        books = soup.find_all('div', class_='image_container')
        for book in books:
            books_url.append(book.find('a')['href'].split('../')[-1])

        next_page_btn = soup.find('li', class_='next')

        if next_page_btn:
            url_next = next_page_btn.find('a')['href']
            scrapped_url = urljoin(scrapped_url, url_next)
        else:
            scrapped_url = None

    else:
        html = get_html(scrapped_url)
        books_url.append(scrapped_url.split('../')[-1])
        scrapped_url = None


# Get all product information
if is_category:
    base_product_url += 'catalogue/'


for book in books_url:
    url = urljoin(base_product_url, book)
    if is_all_product:
        if not url.__contains__('catalogue/'):
            url = urljoin(base_product_url+'catalogue/', book)

    html = get_html(url)

    print('*', end='', flush=True)
    data.append(get_product_information(html, url))
    i += 1


if len(data) > 0:
    generate_file(data, is_category, is_all_product)
    print('\nSuccessfully saved CSV file')

# export products by categories
if is_all_product:
    all_products_file = pd.read_csv('extract/extract_all_products.csv')
    generate_all_category_files(all_products_file)
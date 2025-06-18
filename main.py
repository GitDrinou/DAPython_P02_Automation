import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from csv_writer import write_file
from scraping import get_product_information, get_html

is_category = False
books_url = []
data = []
i = 0

# TODO: change to a Prompt user
scrapped_url = 'https://books.toscrape.com/catalogue/category/books/mystery_3/'
base_product_url = 'https://books.toscrape.com/catalogue/'

while scrapped_url:
    for item in scrapped_url.split('/'):
        if item == 'category':
            is_category = True
            break

    if is_category:

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
print('Loading...')
for book in books_url:
    url = urljoin(base_product_url, book)
    html = get_html(url)

    print('*', end='', flush=True)
    data.append(get_product_information(html, url))
    i += 1


if len(data) > 0:
    write_file(data, is_category)
    print('\nSuccessfully saved the data')
import requests
import re
from bs4 import BeautifulSoup

scrap_url = 'https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html'

r = requests.get(scrap_url)

status_code = r.status_code

if status_code == 200:
    print('Successfully scraped')
    soup = BeautifulSoup(r.content, 'html.parser')
    soup.prettify()

    title = soup.h1.string

    # Refactor to function
    upc = soup.find('th', string='UPC').find_next_sibling().string
    price_including_tax = soup.find('th', string='Price (incl. tax)').find_next_sibling().string
    price_excluding_tax = soup.find('th', string='Price (excl. tax)').find_next_sibling().string
    availability = soup.find('th', string='Availability').find_next_sibling()
    product_description = soup.find(id='product_description').find_next_sibling().string
    reviews = soup.find('th', string='Number of reviews').find_next_sibling().string

    number_availability = re.findall(r'\d+', availability.string)

    links = soup.find('ul', class_='breadcrumb').find_all('li')
    category = links[-2].find('a').string

    images = soup.findAll('img')
    image_url = ''
    for image in images:
        alternate_text = image.attrs['alt']
        if alternate_text is not None and alternate_text == title:
            image_url = image['src']

    book = {
        'product_page_url': scrap_url,
        'universal_product_code': upc,
        'title': title,
        'price_including_tax': price_including_tax,
        'price_excluding_tax': price_excluding_tax,
        'category': category,
        'review_rating': reviews,
        'image_url': image_url,
    }
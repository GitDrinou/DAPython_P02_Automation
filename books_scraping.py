import requests
import re
from bs4 import BeautifulSoup

scrap_url = 'https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html'

r = requests.get(scrap_url)
status_code = r.status_code

def get_fields(name, tag = '', is_id = False):
    if is_id:
        return soup.find(id=name).find_next_sibling().string
    else:
        return soup.find(tag, string = name).find_next_sibling().string

if status_code == 200:
    print('Successfully scraped')
    soup = BeautifulSoup(r.content, 'html.parser')
    soup.prettify()

    title = soup.h1.string
    number_availability = re.findall(r'\d+', availability.string)

    links = soup.find('ul', class_='breadcrumb').find_all('li')
    category = links[-2].find('a').string

    images = soup.find_all('img')
    image_url = ''
    for image in images:
        alternate_text = image.attrs['alt']
        if alternate_text is not None and alternate_text == title:
            image_url = image['src']

    book = {
        'product_page_url': scrap_url,
        'universal_product_code': get_fields('UPC', 'th'),
        'title': title,
        'price_including_tax': get_fields('Price (incl. tax)', 'th'),
        'price_excluding_tax': get_fields('Price (excl. tax)', 'th'),
        'number_available': get_fields('Availability', 'th'),
        'product_description':get_fields('product_description', '', True),
        'category': category,
        'review_rating': get_fields('Number of reviews', 'th'),
        'image_url': image_url,
    }
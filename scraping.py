import re

import requests
from bs4 import BeautifulSoup

def get_html(page_url):
    """Get html from url"""
    r = requests.get(page_url)
    if r.status_code == 200:
         return r.content
    else:
        return print('Failed to scrap the page')

def get_product_information(html, url):
    """Generate a dictionary of product information."""
    soup = BeautifulSoup(html, 'html.parser')
    soup.prettify()

    def get_fields(name, tag='', is_id=False):
        """Get the text for next sibling HTML element of selected tag or id"""
        if is_id:
            if soup.find(id=name) is not None:
                return soup.find(id=name).find_next_sibling().string
            return ''
        else:
            return soup.find(tag, string=name).find_next_sibling().string

    title = soup.h1.string
    availability = get_fields('Availability', 'th')
    number_available = re.findall(r'\d+', availability)[0]
    links = soup.find('ul', class_='breadcrumb').find_all('li')
    category = links[-2].find('a').string

    images = soup.find_all('img')
    image_url = ''
    for image in images:
        alternate_text = image.attrs['alt']
        if alternate_text is not None and alternate_text == title:
            image_url = image['src']

    book_info = {
        'product_page_url': url,
        'universal_product_code': get_fields('UPC', 'th'),
        'title': title,
        'price_including_tax': get_fields('Price (incl. tax)', 'th'),
        'price_excluding_tax': get_fields('Price (excl. tax)', 'th'),
        'number_available': number_available,
        'product_description': get_fields('product_description', '', True),
        'category': category,
        'review_rating': get_fields('Number of reviews', 'th'),
        'image_url': image_url,
    }

    return book_info
import re
import requests
from bs4 import BeautifulSoup
from enum import Enum
from generate_file import download_images

class Rating(Enum):
    ONE = 1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5

def get_content(page_url):
    """Get html from url"""
    r = requests.get(page_url)
    if r.status_code == 200:
         return r.content
    else:
        return print('Erreur: impossible de traiter la page.')

def get_product_information(html, url, base_url, is_category = False):
    """Generate a dictionary of product information."""
    soup = BeautifulSoup(html, 'html.parser')
    soup.prettify()

    def get_fields(name, tag = '', is_id = False, is_rating = False):
        """Get the text for next sibling HTML element of selected tag or id"""
        if is_id:
            if soup.find(id=name) is not None:
                return soup.find(id=name).find_next_sibling().string
            return ''
        elif is_rating:
            rating = soup.find(tag, class_=name).get('class')
            value_rating = 0
            if len(rating) > 1:
                for enum in Rating:
                    if enum.name == rating[1].upper():
                        value_rating = enum.value
            return value_rating
        else:
            return soup.find(tag, string=name).find_next_sibling().string

    upc = get_fields('UPC', 'th')
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
            image_url = image['src'].split('../../')[-1]

    book_info = {
        'product_page_url': url,
        'universal_product_code': upc,
        'title': title,
        'price_including_tax': get_fields('Price (incl. tax)', 'th'),
        'price_excluding_tax': get_fields('Price (excl. tax)', 'th'),
        'number_available': number_available,
        'product_description': get_fields('product_description', '', True),
        'category': category,
        'review_rating': get_fields('star-rating', 'p', False,True),
        'image_url': image_url,
    }

    # download image locally
    base_url = base_url.removesuffix('catalogue/')
    download_images(f'{base_url}{image_url}', upc , category)

    return book_info
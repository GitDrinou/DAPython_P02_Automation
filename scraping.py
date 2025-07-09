import re
import requests
from bs4 import BeautifulSoup
from generate_file import download_images

def get_content(page_url):
    """Get html from url"""
    r = requests.get(page_url)
    if r.status_code == 200:
         return r.content
    else:
        return print('Error: Unable to process the page.')

def get_rating(rating):
    """Get the rating value from a class name"""
    ratings = {
        'ONE': 1,
        'TWO': 2,
        'THREE': 3,
        'FOUR': 4,
        'FIVE': 5
    }
    value_rating = 0
    if len(rating) > 1:
        for item in ratings:
            if item == rating[1].upper():
                value_rating = ratings[item]
    return value_rating

def get_product_information(html, url, base_url):
    """Generate a dictionary of product information."""
    soup = BeautifulSoup(html, 'html.parser')
    soup.prettify()

    upc = soup.find('th', string='UPC').find_next_sibling().string
    title = soup.h1.string
    price_with_tax = soup.find('th', string='Price (incl. tax)').find_next_sibling().string
    price_without_tax = soup.find('th', string='Price (excl. tax)').find_next_sibling().string
    availability = soup.find('th', string='Availability').find_next_sibling().string
    price_amount_with_tax = f"£{float(price_with_tax[1:]):,.2f}"
    price_amount_without_tax = f"£{float(price_without_tax[1:]):,.2f}"
    number_available = re.findall(r'\d+', availability)[0]
    description = soup.find(id='product_description')
    product_description = ''
    if description is not None:
        product_description = description.find_next_sibling().string
    else:
        product_description = ''

    links = soup.find('ul', class_='breadcrumb').find_all('li')
    category = links[-2].find('a').string

    rating = soup.find('p',class_='star-rating').get('class')


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
        'price_including_tax': price_amount_with_tax,
        'price_excluding_tax': price_amount_without_tax,
        'number_available': number_available,
        'product_description': product_description,
        'category': category,
        'review_rating': get_rating(rating),
        'image_url': base_url + image_url,
    }

    # download image locally
    base_url = base_url.removesuffix('catalogue/')
    download_images(f'{base_url}{image_url}', upc , category)

    return book_info
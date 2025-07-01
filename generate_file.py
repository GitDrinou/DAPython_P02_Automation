import pandas as pd
import os
import re
import urllib.request

from datetime import datetime
from soupsieve.util import lower

current_date_time = datetime.now().strftime("%Y%m%d_%H%M%S")
current_date = datetime.now().strftime("%Y%m%d")

def generate_file(datalist, is_category=False, is_all_product=False):

    headers = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_excluding_tax',
               'number_available', 'product_description', 'category', 'review_rating', 'image_url']

    if is_category:
        file_name = f'extract/extract_one_category_{current_date_time}.csv'
    elif is_all_product:
        file_name = 'extract/extract_all_products.csv'
    else:
        file_name = f'extract/extract_one_product_{current_date_time}.csv'

    df = pd.DataFrame(datalist, columns=headers)
    df.to_csv(file_name, sep=',', header=True, index=False, encoding='utf-8')

def generate_all_category_files(df):
    if 'category' not in df.columns:
        print('Aucune catégorie trouvée')

    for category_name in df['category'].unique():
        category = df[df['category'] == category_name]
        prefix = re.sub(" ", "_", lower(category_name))
        file_name = f'extract/by_category/{prefix}_{current_date_time}.csv'
        category.to_csv(file_name, index=False)

def download_images(url, book_upc, book_category):
    os.makedirs('extract/images/' + book_category + '/', exist_ok=True)
    file_name = f'{book_upc}.jpg'
    urllib.request.urlretrieve(url, 'extract/images/' + book_category + '/' + file_name )
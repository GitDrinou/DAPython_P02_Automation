import csv
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

    with open(file_name, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, delimiter=',',fieldnames=headers)
        writer.writeheader()
        writer.writerows(datalist)

def generate_all_category_files(df):
    if 'category' not in df.columns:
        print('No category found')

    for category_name in df['category'].unique():
        category = df[df['category'] == category_name]
        prefix = re.sub(" ", "_", lower(category_name))
        file_name = f'extract/by_category/{prefix}_{current_date_time}.csv'
        category.to_csv(file_name, index=False)

def download_images(url, file_name):
    urllib.request.urlretrieve(url, 'extract/images/' + file_name)
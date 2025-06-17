import csv

from datetime import datetime

def write_file(datalist, is_category=False):

    current_date = datetime.now().strftime("%Y%m%d_%H%M%S")

    headers = ['product_page_url', 'universal_product_code', 'title', 'price_including_tax', 'price_excluding_tax',
               'number_available', 'product_description', 'category', 'review_rating', 'image_url']

    if is_category:
        file_name = 'extract/extract_category_'+ current_date +'.csv'
    else:
        file_name = 'extract/extract_one_product_'+ current_date + '.csv'

    with open(file_name, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, delimiter=',',fieldnames=headers)
        writer.writeheader()
        writer.writerows(datalist)
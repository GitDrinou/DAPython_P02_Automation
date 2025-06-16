import requests

scrap_url = 'https://books.toscrape.com/catalogue/sapiens-a-brief-history-of-humankind_996/index.html'

r = requests.get(scrap_url)

status_code = r.status_code

if status_code == 200:
    print('Successfully scraped')


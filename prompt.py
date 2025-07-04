def ask_url():
    url_to_scrape = input("Please enter the URL: ").strip()
    if url_to_scrape.endswith(".html"):
        return url_to_scrape.rsplit("/", 1)[0] + "/"
    elif not url_to_scrape.endswith("/"):
        return url_to_scrape + "/"
    else:
        return url_to_scrape
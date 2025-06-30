def ask_url():
    while True:
        url_to_scrape = input("Veuillez entrer l'URL de la page à scraper: ").strip()
        if url_to_scrape.endswith(".html"):
            print("ERREUR: l'URL ne doit pas se terminer avec la page html. Veuillez réessayer.")
            continue

        if not url_to_scrape.endswith("/"):
            print("ERREUR: l'URL doit se terminer par un '/'. Veuillez réessayer.")
            continue

        return url_to_scrape
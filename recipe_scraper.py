import requests
from bs4 import BeautifulSoup
from recipe_scrapers import scrape_html
import pandas as pd

def append_json_to_csv(json_data, csv_file):
    df = pd.json_normalize(json_data)
    try:
        with open(csv_file, 'r') as file:
            df.to_csv(csv_file, mode='a', header=False, index=False)
    except FileNotFoundError:
        df.to_csv(csv_file, mode='w', header=True, index=False)

recipes_html = requests.get("https://www.allrecipes.com/recipes-a-z-6735880").text
recipes_soup = BeautifulSoup(recipes_html, 'lxml')

recipes = recipes_soup.find_all('a', class_ = 'mntl-link-list__link type--dog-link type--dog-link')

for category in recipes:
    cat_link = category['href']
    cat_soup = BeautifulSoup(requests.get(cat_link).text, 'lxml')

    recipe_links= cat_soup.find_all('a', class_='comp mntl-card-list-items mntl-document-card mntl-card card card--no-image')
    for link in recipe_links:
        url = link['href']
        html = requests.get(url=url, headers={"User-Agent": f"Burger Seeker"}).content
        scraper = scrape_html(html, org_url=url)
        append_json_to_csv(scraper.to_json(),"recipe_data.csv")

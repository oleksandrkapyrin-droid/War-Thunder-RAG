import requests
from bs4 import BeautifulSoup


HEADERS = {'User-Agent': 'wt-rag-learning-bot'}

def get_urls(sitemap_url):
    r = requests.get(sitemap_url, headers=HEADERS, timeout=30)
    r.raise_for_status
    soup = BeautifulSoup(r.text, 'xml')
    urls = [loc.text for loc in soup.find_all('loc')]

    return urls


unit_urls = get_urls('https://wiki.warthunder.ru/sitemap-units.xml')
print(len(unit_urls))
print(unit_urls[:3])
import requests
from bs4 import BeautifulSoup


HEADERS = {'User-Agent': 'wt-rag-learning-bot'}

def get_urls(sitemap_url):
    r = requests.get(sitemap_url, headers=HEADERS, timeout=30)
    r.raise_for_status
    soup = BeautifulSoup(r.text, 'xml')
    urls = [loc.text for loc in soup.find_all('loc')]

    return urls


def parse_unit(url):
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status
    soup = BeautifulSoup(r.text, 'lxml')

    if soup.title:
        title = soup.title.get_text(strip=True)
    else:
        title = url

    lines = [title]
    for line in soup.select('div.game-unit_chars-line'):
        header = line.select_one('.game-unit_chars-header')
        value = line.select_one('.game-unit_chars-value')
        if header and value:
            label = header.get_text(' ', strip=True)
            val = value.get_text(' | ', strip=True)
            lines.append(f'{label}: {val}')

    return '\n'.join(lines)



unit_urls = get_urls('https://wiki.warthunder.ru/sitemap-units.xml')
print(len(unit_urls))

text = parse_unit('https://wiki.warthunder.ru/unit/f7f1')
print(text)
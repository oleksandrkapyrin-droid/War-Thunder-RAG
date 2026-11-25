import requests
from bs4 import BeautifulSoup


r = requests.get('https://wiki.warthunder.ru/unit/f7f1',
                 headers={'User-Agent': 'wt-rag-learning-bot'}, timeout=30)
print("Вес: у відповіді?", "Вес:" in r.text)

soup = BeautifulSoup(r.text, 'lxml')
print(repr(soup.title.get_text(strip=True)))

for el in soup.select('div.form-text'):
    print(el.get('class'), '->', el.get_text(' ', strip=True))
import requests
from bs4 import BeautifulSoup


HEADERS = {'User-Agent': 'wt-rag-learning-bot'}

MODE_LABELS = {
    "show-char-rb-mod-ref": "РБ, эталонная",
    "show-char-rb-mod-basic": "РБ, базовая",
    "show-char-ab-mod-ref": "АБ, эталонная",
    "show-char-ab-mod-basic": "АБ, базовая",
}


def get_urls(sitemap_url):
    r = requests.get(sitemap_url, headers=HEADERS, timeout=30)
    r.raise_for_status
    soup = BeautifulSoup(r.text, 'xml')
    urls = [loc.text for loc in soup.find_all('loc')]

    return urls


def format_value(value):
    pairs = []

    for span in value.find_all('span'):
        for class_name in span.get('class', []):
            if class_name in MODE_LABELS:
                pairs.append((MODE_LABELS[class_name], span.get_text(strip=True)))
                span.extract()
                break

    unit = value.get_text(' ', strip=True)

    if not pairs:
        return unit

    result = []
    for label, number in pairs:
        result.append(f'{label}: {number} {unit}'.strip())

    return '; '.join(result)


def parse_unit(url):
    r = requests.get(url, headers=HEADERS, timeout=30)
    r.raise_for_status
    soup = BeautifulSoup(r.text, 'lxml')

    title = url
    if soup.title:
        title = soup.title.get_text(strip=True).split('|')[0].strip()

    lines = [f'Техника: {title}']

    for item in soup.select('div.game-unit_card-info_item'):
        label = item.select_one('.game-unit_card-info_title')
        value = item.select_one('.game-unit_card-info_value')
        if label and value:
            label_text = label.get_text(' ', strip=True)
            value_text = value.get_text(' ', strip=True)
            lines.append(f'{label_text}: {value_text}')

    for blok in soup.select('div.form-text, span.game-unit_weapon-title, div.game-unit_chars-line'):
        classes = blok.get('class', [])

        if 'game-unit_chars-line' in classes:
            label = blok.select_one('.game-unit_chars-header')
            value = blok.select_one('.game-unit_chars-value')
            if label and value:
                label_text = label.get_text(' ', strip=True)
                lines.append(f'{label_text}: {format_value(value)}')
        elif 'game-unit_weapon-title' in classes:
            lines.append(f'### Вооружение: {blok.get_text(' ', strip=True)}')
        else:
            text = blok.get_text(' ', strip=True)
            if text.endswith(':'):
                lines.append(f'## {text}')
            elif text:
                lines.append(text)
            

    return '\n'.join(lines)



text = parse_unit('https://wiki.warthunder.ru/unit/f7f1')
print(text)
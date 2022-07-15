import requests
import json
from bs4 import BeautifulSoup
from typing import Dict, List


URL = 'https://ru.wikipedia.org/w/index.php?title=Категория:Животные_по_алфавиту'
ALPHABET = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')


def gen_urls_abc(url: str, abc: set) -> List[str]:
    '''Сгенерировать ссылки начальных страниц по алфавиту'''
    links = []
    for letter in abc:
        link = f'{url}&from={letter}'
        links.append(link)
    return links


def parsing_one_group(url: str) -> Dict[str, list[str]]:
    '''
    Парсинг одной группы по букве.
    Возвращает список животных в словаре
    {"А": "Аардоникс"}
    '''
    page = requests.get(url).text
    soup = BeautifulSoup(page, 'lxml')
    group = soup.find(id='mw-pages').find('div', class_='mw-category-group')
    letter = group.find('h3').text
    animals = {letter: []}
    while letter == group.find('h3').text:
        animals_list = group.find('ul').find_all('li')
        print(f'Парсим категорию {letter}')
        for animal in animals_list:
            animals[letter].append(animal.text)
        link_next_page_obj = soup.find('a', text='Следующая страница')
        if link_next_page_obj:
            next_page = link_next_page_obj.get('href')
            url = f"https://ru.wikipedia.org/{next_page}"
            page = requests.get(url).text
            soup = BeautifulSoup(page, 'lxml')
            group = soup.find(id='mw-pages').find('div', class_='mw-category-group')
    return animals


def get_animals(url: str, abc: set) -> Dict[str, str]:
    '''
    Получить список животных согласно алфавита abc.
    Вернуть словарь с животными
    '''
    animals = dict()
    links = gen_urls_abc(url, abc)
    for link in links:
        group = parsing_one_group(link)
        animals.update(group)
    return animals


if __name__ == '__main__':
    animals = get_animals(URL, ALPHABET)
    with open('animals.json', 'w', encoding='utf8') as f:
        json.dump(animals, f, indent=2, ensure_ascii=False)

    for i in animals:
        cnt = len(animals[i])
        print(f'{i}: {cnt}')


import asyncio
from os import stat
import aiohttp
import json
import time

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


async def parsing_one_group(session, url: str, animals: dict) -> Dict[str, list[str]]:
    '''
    Парсинг одной группы по букве.
    Возвращает список животных в словаре
    {"А": "Аардоникс"}
    '''
    async with session.get(url=url) as response:
        page = await response.text()
        soup = BeautifulSoup(page, 'lxml')
        group = soup.find(id='mw-pages').find('div', class_='mw-category-group')
        letter = group.find('h3').text
        while letter == group.find('h3').text:
            animals_list = group.find('ul').find_all('li')
            print(f'\rПарсим категорию {letter}', end='')
            for animal in animals_list:
                animals.setdefault(letter, []).append(animal.text)
            link_next_page_obj = soup.find('a', text='Следующая страница')
            if link_next_page_obj:
                next_page = link_next_page_obj.get('href')
                url = f"https://ru.wikipedia.org/{next_page}"
                async with session.get(url=url) as response:
                    page = await response.text()
                    soup = BeautifulSoup(page, 'lxml')
                    group = soup.find(id='mw-pages').find('div', class_='mw-category-group')
    return animals



async def get_animals(url: str, abc: set) -> Dict[str, str]:
    '''
    Получить список животных согласно алфавита abc.
    Вернуть словарь с животными
    '''
    async with aiohttp.ClientSession() as session:
        tasks = []
        animals = dict()
        links = gen_urls_abc(url, abc)
        for link in links:
            task = asyncio.create_task(parsing_one_group(session, link, animals))
            tasks.append(task)
        await asyncio.gather(*tasks)
    return animals


if __name__ == '__main__':
    start_time = time.time()
    animals = asyncio.run(get_animals(URL, ALPHABET))
    end_time = time.time() - start_time
    print(f'\nВремя выполнения парсинга {end_time} сек.')
    with open('animals.json', 'w', encoding='utf8') as f:
        json.dump(animals, f, indent=2, ensure_ascii=False)

    for i in animals:
        cnt = len(animals[i])
        print(f'{i}: {cnt}')


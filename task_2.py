import requests
from bs4 import BeautifulSoup


url = 'https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту'
page = requests.get(url).text
animals = dict()
parsing = True
alphabet = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')

while parsing:
    soup = BeautifulSoup(page, 'lxml')
    groups = soup.find(id='mw-pages').find_all('div', class_='mw-category-group')
    for group in groups:
        category_name = group.find('h3').text
        if not alphabet.isdisjoint(category_name.lower()):
            print(f'Парсим категорию {category_name}')
            animals_list = group.find('ul').find_all('li')
            for animal in animals_list:
                name = animal.text
                animals.setdefault(category_name, []).append(name)
        else:
            print(f'Пропускаем {category_name}')
    link_next_page = soup.find('a', text='Следующая страница')
    if link_next_page:
        url = f"https://ru.wikipedia.org/{link_next_page.get('href')}"
        page = requests.get(url).text
    else:
        parsing = False


for i in animals:
    print(f'{i}: {len(animals[i])}')


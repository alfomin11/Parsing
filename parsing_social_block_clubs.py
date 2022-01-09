"""
Собрать ссылки на соц.сети всех футбольных клубов Российской Премьер-Лиги
"""


import requests
from bs4 import BeautifulSoup
import json

url = "https://premierliga.ru/clubs/"


def request(url):
    req = requests.get(url)  # запрос

    # для проверки правильности выведем html код страницы
    source = req.text
    #print(source)

    # сохраним страницу в файл
    with open("index.html", "w") as file:
        file.write(source)


request(url)

# прочитаем сохраненный файл и сохраним в переменную
with open("index.html") as file:
    source = file.read()

soup = BeautifulSoup(source, "lxml")

cur_season_table = soup.find("div", class_="cur-season-table")
#print(cur_season_table)

#for item in cur_season_table:
#    print(item)

# будем получать ссылки на клубы по классу logo
class_logo_all = soup.find_all("td", class_="logo")
#print(class_logo_all)

# выведем полученный результат
#for item in class_logo_all:
#  print(item)

# соберем ссылки на страницы клубов (href)
all_club = []  # будем сохранять ссылки на страницы в список

for item in class_logo_all:
    all_href = item.find("a")
    item_href = "https://premierliga.ru/" + all_href.get("href")
    all_club.append(item_href)
#print(all_club)

# сохраняем результаты парсинга в словарь
social_block_clubs_dict = {}  # словарь (название клуба: список ссылок на соц.сети)

# перейдем на страницу каждого клуба и соберем ссылки на их соц.сети
for club in all_club:
    url_club = club

    req_club = requests.get(url_club) # запрос

    source_club = req_club.text

    # сохраним страницу в файл, чтобы не делать миллион запросов на сайт
    with open("index_clubs.html", "w") as file:
        file.write(source_club)

    # прочитаем сохраненный файл и сохраним в переменную
    with open("index_clubs.html") as file:
        source_club = file.read()

    soup_club = BeautifulSoup(source_club, "lxml")

    social_block_club = soup_club.find("div", class_="social-block")

    # будем сохранять ссылки на соц.сети в список
    social_block_club_list = []

    # соберем ссылки на соц.сети
    club_href = social_block_club.find_all("a")
    for item in club_href:
        item_href = item.get("href")
        social_block_club_list.append(item_href)

    # сохраним название клуба
    title_club = soup_club.find("div", class_="title-club")
    title = title_club.find("h1").text

    # добавляем в словарь
    social_block_clubs_dict[title] = social_block_club_list

# сохраним данные в json файл
with open("social_block_clubs_dict.json", "w", encoding="utf-8") as file:
    json.dump(social_block_clubs_dict, file, indent=4, ensure_ascii=False)


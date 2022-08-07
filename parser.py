import csv
import time
from urllib import response
import requests
from bs4 import BeautifulSoup


def get_text_from_data(data, tag, class_):
    query = data.find_all(tag, class_)
    result = []
    for item in query:
        result.append(item.text.strip().replace(u'\xa0', u' '))
    return result

def get_link_from_data(data, tag, class_):
    main_url = 'https://nambafood.kg'
    query = data.find_all(tag, class_, href=True)
    result = []
    for item in query:
        result.append(main_url + item['href'])
    return result

def get_image_from_data(data, tag, class_):
    main_url = 'https://nambafood.kg'
    query = data.find_all(tag, class_)
    result = []
    for item in query:
        image = item.find('img')
        result.append(main_url + image['src'])
    return result

def main():
    cafe_urls = 'https://nambafood.kg/cafe'
    response_cafes_urls = requests.get(cafe_urls)
    catalog = BeautifulSoup(response_cafes_urls.text, 'lxml')

    cafe_urls = get_link_from_data(catalog, 'a', 'cafe-item')
    tmp_count = 0
    with open("out.csv", mode="w", encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter = ",", lineterminator="\r")
        file_writer.writerow(['Кафе', 'Категория', 'Блюдо', 'Описание', 'Цена'])
        for cafe_url in cafe_urls:
            if tmp_count < 3:

                response_cafe_url = requests.get(cafe_url)
                cafe_response = BeautifulSoup(response_cafe_url.text, 'lxml')
                cafe_name = get_text_from_data(cafe_response, 'h1', 'cafe--name')
                categories = get_text_from_data(cafe_response, 'h2', 'title')
                titles = get_text_from_data(cafe_response, 'div', 'card--item--title')
                images = get_image_from_data(cafe_response, 'div', 'card--item--prev')
                descriptions = get_text_from_data(cafe_response, 'div', 'card--item--description')
                prices = get_text_from_data(cafe_response, 'div', 'price')
                for category in categories:
                        for count, title in enumerate(titles):
                            cafe_item = []

                            cafe_item.append(cafe_name[0])
                            cafe_item.append(category)
                            cafe_item.append(titles[count])
                            cafe_item.append(images[count])
                            cafe_item.append(descriptions[count])
                            cafe_item.append(prices[count])
                            file_writer.writerow(cafe_item)

            tmp_count += 1

if __name__ == '__main__':
    tic = time.perf_counter()
    main()
    toc = time.perf_counter()
    print(f"Парсинг занял {toc - tic:0.4f} секунд")

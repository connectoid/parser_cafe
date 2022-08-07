import csv
from urllib import response
import requests
from bs4 import BeautifulSoup

main_url = 'https://nambafood.kg'
cafe_urls = 'https://nambafood.kg/cafe'
response_cafes_urls = requests.get(cafe_urls)
catalog = BeautifulSoup(response_cafes_urls.text, 'lxml')



def get_text_from_data(data, tag, class_):
    query = data.find_all(tag, class_)
    result = []
    for item in query:
        result.append(item.text.strip().replace(u'\xa0', u' '))
    return result

def get_link_from_data(data, tag, class_):
    query = data.find_all(tag, class_, href=True)
    result = []
    for item in query:
        result.append(main_url+item['href'])
    return result

def get_image_from_data(data, tag, class_):
    query = data.find_all(tag, class_)
    result = []
    for item in query:
        result.append(item['src'])
    return result

cafe_urls = get_link_from_data(catalog, 'a', 'cafe-item')
tmp_count = 0
with open("out.csv", mode="w", encoding='utf-8') as w_file:
    file_writer = csv.writer(w_file, delimiter = ",", lineterminator="\r")
    file_writer.writerow(['Кафе', 'Категория', 'Блюдо', 'Описание', 'Цена'])
    for cafe_url in cafe_urls:
        if tmp_count < 1:

            response_cafe_url = requests.get(cafe_url)
            #print('###### ', cafe_url)
            cafe_response = BeautifulSoup(response_cafe_url.text, 'lxml')
            cafe_name = get_text_from_data(cafe_response, 'h1', 'cafe--name')
            categories = get_text_from_data(cafe_response, 'h2', 'title')
            #print('!!!!!!!! categories in url ', categories)
            titles = get_text_from_data(cafe_response, 'div', 'card--item--title')
            images = get_image_from_data(cafe_response, 'img', 'card--item--prev')
            descriptions = get_text_from_data(cafe_response, 'div', 'card--item--description')
            prices = get_text_from_data(cafe_response, 'div', 'price')
            for category in categories:
                    #print(category)
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


#cafes = get_text_from_data(catalog, 'div', 'cafe--name')
#categories = get_text_from_data(soup, 'h2', 'title')
#titles = get_text_from_data(soup, 'div', 'card--item--title')
#descriptions = get_text_from_data(soup, 'div', 'card--item--description')
#prices = get_text_from_data(soup, 'div', 'price')

#print(categories)
#print(titles)
#print(descriptions)
#print(prices)

""" with open("out.csv", mode="w", encoding='utf-8') as w_file:
    file_writer = csv.writer(w_file, delimiter = ",", lineterminator="\r")
    file_writer.writerow(['Кафе', 'Категория', 'Блюдо', 'Описание', 'Цена'])

    for cafe in cafes:
        for category in categories:
            cafe_item = []
            for count, title in enumerate(titles):
                file_writer.writerow([cafe, category, titles[count], descriptions[count], prices[count]])

                cafe_item.append(category)
                cafe_item.append(titles[count])
                cafe_item.append(descriptions[count])
                cafe_item.append(prices[count])
            cafe1.append(cafe_item) """

#print(cafe_urls)


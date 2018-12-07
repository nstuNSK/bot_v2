import requests
import json
import database as data
from datetime import datetime
tags = ['<strong>', '</strong>', '<p>', '</p>', '</a>', '>', '\n']
connection = data.connect()

def get_actual_url():
    time = datetime.now()
    url = "https://api.ciu.nstu.ru/v1.0/news/schoolkids/"+str(time.year)+"/"+str(time.month)+"/"+str(time.day)#+"?json_indent=1&decode_unicode_escape=1"
    return url

def get_html(url):
    try:
        html = requests.get(url)
    except:
        html = "bad html"
    return html


def get_json(text):
    return json.loads(text)

def send_news(news):
    people = data.get_fields(connection = connection, table_name = "USERS", select_field = "ID_VK", field = "SUB_S", value = True)
    for human in people:
        print(human)

def main():
   url = get_actual_url()
   html = get_html(url)
   text = html.text
   news = get_json(text)
   send_news(news)
   
   for item in news:
       print('Статья: ',item['TITLE'])
       print('ID: ',item['ID'])
       print('Ссылка: ',item['URL'])
       print('Дата: ',item['NEWS_DATE'])
       print('Коротко: ',item['SHORTTEXT'])
    
    




if __name__ == '__main__':
    main()


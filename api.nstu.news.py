import vk_api
import requests
import json
import database as data
import getter
import keyboards
from datetime import datetime

tags = ['<strong>', '</strong>', '<p>', '</p>', '</a>', '>', '\n']
connection = data.connect()

def auth():
    token = getter.get_token()
    print(token)
    vk = vk_api.VkApi(token=token)
    vk._auth_token()
    return vk

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

def get_people(type):
    if type == "schoolchild":
        people = data.get_field(connection = connection, table_name = "USERS", select_field = "ID_VK", field = "SUB_S", value = True)
    else:
        people = data.get_field(connection = connection, table_name = "USERS", select_field = "ID_VK", field = "SUB_E", value = True)
    return people

def create_msgs(news):
    msg = ""
    msgs = []
    for one_news in news:
        if len(msg)<3500:
            msg = msg + "Статья: "+one_news['TITLE'] + "\nПосмотреть можно здесь: " + one_news['URL']+"\n \n"
        else:
            msgs.append(msg)
            msg = ""
    msgs.append(msg)
    return msgs


def send_news(news, vk, type):
    people = get_people(type)
    msgs = create_msgs(news)
    for id in people:
        print("Отправляю новости для: ",type, " на", id[0])
        vk.method("messages.send", {"user_id": id[0], "message": "Вот, принес тебе последние новости😊"})
        for msg in msgs:
            vk.method("messages.send", {"user_id": id[0], "message": msg})
        vk.method("messages.send", {"user_id": id[0], "message": "Пока все😊"})
    people = 
    

    

def main():
   vk = auth() 
   url = get_actual_url()
   html = get_html(url)
   text = html.text
   news = get_json(text)
   send_news(news, vk, "schoolchild")
   send_news(news, vk, "enrollee")
   '''for item in news:
       print('Статья: ',item['TITLE'])
       print('ID: ',item['ID'])
       print('Ссылка: ',item['URL'])
       print('Дата: ',item['NEWS_DATE'])
       print('Коротко: ',item['SHORTTEXT'])'''
    
    




if __name__ == '__main__':
    main()


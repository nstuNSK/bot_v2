import vk_api
import requests
import time
import json
import database as data
import getter
import keyboards
from datetime import datetime

connection = data.connect()

def auth():
    token = getter.get_token()
    print(token)
    vk = vk_api.VkApi(token=token)
    vk._auth_token()
    return vk

vk = auth()

def get_actual_url():
    time = datetime.now()
    url = "https://api.ciu.nstu.ru/v1.0/news/schoolkids/"+str(time.year)+"/"+str(time.month)+"/"+str(time.day)
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
    

def send_one_person(id, type):
    url = get_actual_url()
    html = get_html(url)
    text = html.text
    news = get_json(text)
    msgs = create_msgs(news)
    print("Только одному!")
    print("Отправляю новости для: ",type, " на", id)
    vk.method("messages.send", {"user_id": id, "message": "Вот, принес тебе последние новости😊"})
    for msg in msgs:
        vk.method("messages.send", {"user_id": id, "message": msg})
    vk.method("messages.send", {"user_id": id, "message": "Пока все😊"})

def main():
    i = 1
    f = open("logs.txt", "a")
    while True:
        if i == 2:
            f.write("end script")
            f.close()
            break
        f.write("time: " + str(datetime.now())+"\n")
        f.write(str(i)+") ")
        i = i+1
        url = get_actual_url()
        f.write("New url!!! " + str(url)+"\n")
        html = get_html(url)
        f.write("New html added!!!"+"\n")
        text = html.text
        news = get_json(text)
        f.write("News created!!!"+"\n")
        #send_news(news, vk, "schoolchild")
        #send_news(news, vk, "enrollee")
        time.sleep(30)
        '''for item in news:
        print('Статья: ',item['TITLE'])
        print('ID: ',item['ID'])
        print('Ссылка: ',item['URL'])
        print('Дата: ',item['NEWS_DATE'])
        print('Коротко: ',item['SHORTTEXT'])'''


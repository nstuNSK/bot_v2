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
    f = open("logs.txt", "a")
    token = getter.get_token()
    try:
        vk = vk_api.VkApi(token=token)
        vk._auth_token()
        f.write("auth successful!\n")
    except:
        vk = None
        f.write("Error: auth failed!\n")
        f.close()
        return vk
    f.close()
    return vk

vk = auth()

def get_actual_url():
    time = datetime.now()
    url = "https://api.ciu.nstu.ru/v1.0/news/schoolkids/2018/12/4"#+str(time.year)+"/"+str(time.month)+"/"+str(time.day)
    return url

def get_html(url):
    f = open("logs.txt", "a")
    try:
        html = requests.get(url)
    except:
        html = None
        f.write("Error: bad html\n")
        return html
    f.close()
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
    f = open("logs.txt", "a")
    people = get_people(type)
    msgs = create_msgs(news)
    f.write("starting send for " + str(type)+"\n")
    for id in people:
        f.write("send to: " + str(id[0])+"\n")
        vk.method("messages.send", {"user_id": id[0], "message": "Вот, принес тебе последние новости😊"})
        f.write("title msg sended\n")
        for msg in msgs:
            vk.method("messages.send", {"user_id": id[0], "message": msg})
            f.write("news sended\n")
        vk.method("messages.send", {"user_id": id[0], "message": "Пока все😊"})
        f.write("footer msg sended\n")
    f.close()
    

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
    f.write("////////////\nnew log:\ntime: " + str(datetime.now())+"\n")
    url = get_actual_url()
    f.write("url: " + str(url)+"\n")
    html = get_html(url)
    f.write("html created"+"\n")
    text = html.text
    news = get_json(text)
    last_news = news[0]['NEWS_DATE']
    print(last_news)
    if news != []:
        f.write("news object created"+"\n")
        send_news(news, vk, "schoolchild")
        f.write("send to schoolchild finished"+"\n")
        send_news(news, vk, "enrollee")
        f.write("send to enrollee finished"+"\n"+"////////////\n \n")
    else:
         f.write("News are empty\n")
    f.write("end log\n \n")
    f.close()
    '''for item in news:
    print('Статья: ',item['TITLE'])
    print('ID: ',item['ID'])
    print('Ссылка: ',item['URL'])
    print('Дата: ',item['NEWS_DATE'])
    print('Коротко: ',item['SHORTTEXT'])'''

if __name__ == "__main__":
    main()
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
import vk_api
import random
import time
import json
import sys
import requests
import database as data
import getter
import keyboards
import api_nstu_news as api
def auth():
    token = getter.get_token()
    print(token)
    vk = vk_api.VkApi(token=token)
    vk._auth_token()
    return vk

def subscribe(type, id):
    if data.get_field(connection=connection, table_name="USERS",select_field = type, field="ID_VK", value=id)[0][0]==False:
        data.set_field(connection = connection, table_name = "USERS", ID_VK = id, field = type, value = "1")
        vk.method("messages.send", {"user_id": id, "message": "Теперь я буду отправлять тебе новости! Люблю это😍", 'keyboard': key['main_menu']})
    else:
        data.set_field(connection = connection, table_name = "USERS", ID_VK = id, field = type, value = "0")
        vk.method("messages.send", {"user_id": id, "message": "Не хочешь, как хочешь...\nНо, если передумаешь, я всегда готов💪🏻", 'keyboard': key['main_menu']})

def search_direction_by_subjects(id):
    print("yeah!")
    res = []
    sb2 = data.get_field(select_field = "SUBJECT2",table_name = "USERS",connection= connection,value=id, field="id_vk")[0][0]
    if sb2 == 0:
        vk.method("messages.send", {"user_id": id, "message": "Кажется ты забыл выбрать предметы... Давай, исправляйся😊", "keyboard":key['subjects']})
    else:
        res = data.get_field(select_field = "DIRECTION, PROFILE_NAME, FACULT, DESCR, URL",table_name = "DIRECTIONS",connection= connection,value=sb2, field="DISC2") 
        sb3 = data.get_field(select_field = "SUBJECT3",table_name = "USERS",connection= connection,value=id, field="id_vk")[0][0]
        if sb3!=0:
            temp = data.get_field(select_field = "DIRECTION, PROFILE_NAME, FACULT, DESCR, URL",table_name = "DIRECTIONS",connection= connection,value=sb3, field="DISC3")
            if temp != 0:
                for item in temp:
                    res.append(item)
        res = list(set(res))
        vk.method("messages.send", {"user_id": id, "message": "Понеслась!"})
        response = ""
        for item in res:
            if item[1]=='None':
                if item[3]=='null':
                    response = response + "Направление: " + '"' + item[0] + '"' + " на факультете " + item[2]+ "\n" +"Ссылка на направление: " + item[4]+"\n\n"
                else:
                    response = response + "Направление: " + '"' + item[0] + '"' + " на факультете " + item[2]+ "\n" +item[3] + "\n" +"Ссылка на направление: " + item[4]+"\n\n"
            else:
                if item[3]=='null':
                    response = response + "Направление: " + '"' + item[0] + ' (' + item[1] + ')' + '"' + " на факультете " + item[2]+ "\n" +"Ссылка на направление: " + item[4]+"\n\n"
                else:
                    response = response + "Направление: " + '"' + item[0] + ' (' + item[1] + ')' + '"' + " на факультете " + item[2]+ "\n" +item[3] + "\n" +"Ссылка на направление: " + item[4]+"\n\n"
            if(len(response)>3500):
                vk.method("messages.send", {"user_id": id,"message": response})
                response = ""
        if(response!=""):
            vk.method("messages.send", {"user_id": id,"message": response})
        vk.method("messages.send", {"user_id": id,"message": "Заставил же ты меня потрудиться!😁", 'keyboard': key['main_menu']})

def search_direction_by_sphere(id):
    sql = "SELECT NAME, DESCR, FACULTY, URL FROM DIRECTIONS WHERE ID IN (SELECT ID_DIR FROM DIR_SPHERES WHERE ID_SPHERE IN (SELECT ID_SPHERE FROM USERS_SPHERES WHERE ID_USER = "+str(id)+")) GROUP BY ID"
    res = data.executeSQL(sql = sql, connection = connection)
    print("tut")
    if res!=0:
        vk.method("messages.send", {"user_id": id,"message":"Вот что я нашел🙃"})
        response = ""
        for item in res:
            if item[1]=='null':
                response = response + "Направление: " + '"' + item[0] + '"' + " на факультете " + item[2]+ "\n" +"Ссылка на направление: " + item[3]+"\n\n"
            else:
                response = response + "Направление: " + '"' + item[0] + ' (' + item[1] + ')' + '"' + " на факультете " + item[2]+ "\n" +"Ссылка на направление: " + item[3]+"\n\n"
            if(len(response)>3500):
                vk.method("messages.send", {"user_id": id,"message": response})
                response = ""
        if(response!=""):
            vk.method("messages.send", {"user_id": id,"message": response})
        vk.method("messages.send", {"user_id": id,"message": "Искал как в последний раз😂", 'keyboard': key['main_menu']})
    else:
        vk.method("messages.send", {"user_id": id,"message":"А сферы я за тебя добавлять буду?", 'keyboard': key['sphere']})

def add_sphere(id, connection, pay):
    sql = "SELECT ID FROM SPHERES WHERE NAME = '"+str(pay)+"'"
    idSph = data.executeSQL(sql = sql, connection = connection)
    sql = "INSERT INTO USERS_SPHERES (ID_USER, ID_SPHERE) VALUES("+str(id)+", "+str(idSph[0][0])+")"
    data.executeSQL(sql = sql, connection = connection)

#WAIT_FILLING_POINTS = "-3"
#WAIT_FILLING = "-2"
#TEMP_FILLING = "-1"


def data_processing(id, pay, msg):
    if data.search_field(table_name="USERS",connection=connection,value=id, field="ID")==False:
        data.set_user(table_name="USERS", connection=connection,ID_VK=id)
    
    if pay=={"command":"start"} or pay == "admin":
        vk.method("messages.send", {"user_id": id, "message": "Привет, я бот Хван✋🏻\n \nИ я твой персональный помощник в мире НГТУ😎😎😎\n \nЯ могу помочь тебе с поступлением или просто рассказать о НГТУ и обо всем, что с ним связано😎\n \nПравда я пока не самый умный бот, мне еще учиться и учиться, поэтому, пожалуйста, общайся со мной посредством графической клавиатуры (заисключением тех случаев, когда я сам не попрошу написать мне что-нибудь) и тогда все будет чики-пуки🙃"})
        vk.method("messages.send", {"user_id": id, "message": "Итак, чем я могу тебе помочь?", "keyboard": key['main_menu']})
    
    elif msg=="admin":
        vk.method("messages.send", {"user_id": id, "message": "Опять по новой? Ну, ладно...", "keyboard":key['start']})
    
    elif pay == "main_menu":
        vk.method("messages.send", {"user_id": id, "message": "Сделал!", "keyboard":key['main_menu']})

    elif pay=="subscribe":
        vk.method("messages.send", {"user_id": id, "message": "Какие новости нас интересуют?", "keyboard":key['subscribe']})
    
    elif pay=="enrollee":
        subscribe(type = 'SUB_E', id = id)
    
    elif pay=="schoolchild":
        subscribe(type = 'SUB_S', id = id)
    
    elif pay=="direction_selection":
        vk.method("messages.send", {"user_id": id, "message": " А как подобрать напрваление?", "keyboard":key['direction_selection']})
    
    elif pay=="sphere":
        sql = "DELETE FROM USERS_SPHERES WHERE ID_USER = "+str(id)
        data.executeSQL(sql = sql, connection = connection)
        vk.method("messages.send", {"user_id": id, "message": "Подскажи сферы, а то тут много😊", "keyboard":key['sphere']})
    
    elif pay=="Машиностроение" or pay=="Безопасность" or pay=="Энергетика" or pay=="IT-технологии" or pay=="Электроника" or pay=="Авиация" or pay=="Общество" or pay=="Экономика" or pay=="Химия" or pay=="Языки" or pay=="Физика":
        msg = ["Добавил! Это было легко😉", "Проще простого! Добавил!", "Изи добавил!"]
        sql = "SELECT ID_SPHERE FROM USERS_SPHERES WHERE ID_USER = "+str(id)
        size = data.executeSQL(sql = sql, connection = connection)
        if size!=0:
            if len(size) < 3:
                add_sphere(id=id,connection=connection, pay = pay)
                vk.method("messages.send", {"user_id": id, "message": random.choice(msg), "keyboard":key['sphere']})
                if len(size)+1>=3:
                    search_direction_by_sphere(id = id)
        else:
            add_sphere(id=id,connection=connection, pay = pay)
            vk.method("messages.send", {"user_id": id, "message": random.choice(msg), "keyboard":key['sphere']})
        
   
    elif pay=="name_dir":
        data.set_field(connection = connection, table_name = "USERS", ID_VK = id, field = "SUBJECT2", value = 0)
        data.set_field(connection = connection, table_name = "USERS", ID_VK = id, field = "SUBJECT3", value = 0)
        data.set_field(connection = connection, table_name = "USERS", ID_VK = id, field = "SUBJECT4", value = 0)
        vk.method("messages.send", {"user_id": id, "message": "По каким предметам будем искать?\nРусский язык нужен для всех направлений, поэтому я его уже добавил😊", "keyboard":key['subjects']})

    elif pay == "math" or pay == "biology" or pay == "geography" or pay == "foreign_language" or pay == "informatics" or pay == "history" or pay == "literature" or pay == "social_science" or pay == "physics" or pay == "chemistry":
        subject_id = data.get_field(table_name = "SUBJECTS", connection = connection, select_field = 'ID', field = 'SUBJECT', value = pay)[0][0]
        print(subject_id)
        sb2 = data.get_field(table_name = "USERS", connection = connection, select_field = 'SUBJECT2', field = 'ID_VK', value = id)[0][0]
        if sb2==0:
            vk.method("messages.send", {"user_id": id, "message": "Плюс один😉", "keyboard":key['subjects']})
            data.set_field(connection = connection, table_name = 'USERS', ID_VK = id, field = 'SUBJECT2', value = subject_id)
        else:
            sb3 = data.get_field(table_name = "USERS", connection = connection, select_field = 'SUBJECT3', field = 'ID_VK', value = id)[0][0]
            if sb3==0:
                data.set_field(connection = connection, table_name = 'USERS', ID_VK = id, field = 'SUBJECT3', value = subject_id)
                search_direction_by_subjects(id = id)
    
    elif pay == "search_by_sphere":
        search_direction_by_sphere(id = id)
    elif pay == "search_by_subjects":
        search_direction_by_subjects(id = id)
    #elif pay == "name_dir":
        #vk.method("messages.send", {"user_id": id, "message": "Меня пока что этому не научили😞\nНо совсем скоро научат, обещаю!", "keyboard": key['main_menu']})
    elif pay == "lists":
        vk.method("messages.send", {"user_id": id, "message": "Выберите функцию:", "keyboard": key['list']})
    
    elif pay == "lk_code":
        vk.method("messages.send", {"user_id": id, "message": "Меня пока что этому не научили😞\nНо совсем скоро научат, обещаю!", "keyboard": key['main_menu']})
    
    elif pay == "frequency":
        vk.method("messages.send", {"user_id": id, "message": "Меня пока что этому не научили😞\nНо совсем скоро научат, обещаю!", "keyboard": key['main_menu']})
        #vk.method("messages.send", {"user_id": id, "message": "Как часто мне отправлять тебе новости?", "keyboard": key['frequency']})
    
    #elif pay == "one_per_day":
        #vk.method("messages.send", {"user_id": id, "message": "Я буду отправлять тебе", "keyboard":key['main_menu']})

    #elif pay == "two_per_day":
        #vk.method("messages.send", {"user_id": id, "message": "Опять по новой? Ну, ладно...", "keyboard":key['main_menu']})
    elif msg == "Бу!":
        vk.method("messages.send", {"user_id": id, "message": "Аааа!"})
        vk.method("messages.send", {"user_id": id, "message": "А, это ты😃"})
        vk.method("messages.send", {"user_id": id, "message": "Не пугай меня так больше🙏🏻", "keyboard": key['main_menu']})
    else:
        vk.method("messages.send", {"user_id": id, "message": "Я тебя не понимаю😔\nИспользуй, пожалуйста, клавиатуру🙏🏻", "keyboard": key['main_menu']})

def get_msg():
    while True:
        try:
            messages = vk.method("messages.getConversations", {"offset": 0, "count": 100, "filter": "unanswered"})
            if messages["count"] >= 1:
                id = messages["items"][0]["last_message"]["from_id"]
                msg = messages["items"][0]["last_message"]["text"]
                if "payload" in messages["items"][0]["last_message"]:
                    pay = messages["items"][0]["last_message"]["payload"][1:-1]
                    try:
                        pay = bytes(pay, 'cp1251').decode('utf-8')
                    except ValueError:
                        pass
                    finally:
                        print(pay)
                else:
                    pay = "0"
                    print(msg)
                data_processing(id=id, pay=pay, msg=msg)
        except Exception:
            time.sleep(0.1)
                 
key = keyboards.get_keyboards() 

vk = auth()
print(vk)  
connection = data.connect()
print(connection)
get_msg()
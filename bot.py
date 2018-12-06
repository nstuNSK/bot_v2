#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fileencoding=utf-8
import vk_api
import time
import json
import sys
import requests
import database as data
import getter
import keyboards


def auth():
    token = getter.get_token()
    print(token)
    vk = vk_api.VkApi(token=token)
    vk._auth_token()
    return vk

def subscribe(type, id):
    if data.get_field(connection=connection, table_name="USERS",select_field = type, field="ID_VK", value=id)[0][0]==False:
        data.set_field(connection = connection, table_name = "USERS", ID_VK = id, field = type, value = "1")
        vk.method("messages.send", {"user_id": id, "message": "Теперь ты подписан на уведомления", 'keyboard': key['main_menu']})
    else:
        data.set_field(connection = connection, table_name = "USERS", ID_VK = id, field = type, value = "0")
        vk.method("messages.send", {"user_id": id, "message": "Теперь ты отписан от уведомлений", 'keyboard': key['main_menu']})

def search_direction(id):
    res = []
    sphere1 = data.get_field(select_field = "SPHERE1",table_name = "USERS",connection= connection,value=id, field="id_vk")[0][0]
    if sphere1 == 0:
        vk.method("messages.send", {"user_id": id, "message": "Нет добавленных сфер:", "keyboard":key['sphere']})
    else:
        res = data.get_field(select_field = "DIRECTION, PROFILE_NAME, FACULT, DESCR, URL",table_name = "DIRECTIONS",connection= connection,value=sphere1, field="SPHERE")
        sphere2 = data.get_field(select_field = "SPHERE2",table_name = "USERS",connection= connection,value=id, field="id_vk")[0][0]
        if sphere2 != 0:
            temp = data.get_field(select_field = "DIRECTION, PROFILE_NAME, FACULT, DESCR, URL",table_name = "DIRECTIONS",connection= connection,value=sphere2, field="SPHERE")
            if temp != 0:
                for item in temp:
                    res.append(item)
            sphere3 = data.get_field(select_field = "SPHERE3",table_name = "USERS",connection= connection,value=id, field="id_vk")[0][0]
            if sphere3 != 0:
                temp = data.get_field(select_field = "DIRECTION, PROFILE_NAME, FACULT, DESCR, URL",table_name = "DIRECTIONS",connection= connection,value=sphere3, field="SPHERE")
                if temp != 0:
                    for item in temp:
                        res.append(item)
        res = list(set(res))
        response = ""
        vk.method("messages.send", {"user_id": id,"message":"По данным сферам найдены следуюшие направления:"})
        for item in res:
            if item[1]=='null':
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
        vk.method("messages.send", {"user_id": id,"message": "Искал как в последний раз:)", 'keyboard': key['main_menu']})


#WAIT_FILLING_POINTS = "-3"
#WAIT_FILLING = "-2"
#TEMP_FILLING = "-1"


def data_processing(id, pay, msg):
    if data.search_field(table_name="USERS",connection=connection,value=id, field="ID_VK")==False:
        data.set_user(table_name="USERS", connection=connection,ID_VK=id)
    
    if pay=={"command":"start"} or pay == "admin":
        vk.method("messages.send", {"user_id": id, "message": "Привет, я бот Хван✋🏻\n \nИ я твой персональный помощник в мире НГТУ😎😎😎\n \nЯ могу помочь тебе с поступлением или просто рассказать о НГТУ и обо всем, что с ним связано😎\n \nПравда я пока не самый умный бот, мне еще учиться и учиться, поэтому, пожалуйста, общайся со мной посредством графической клавиатуры (заисключением тех случаев, когда я сам не попрошу написать мне что-нибудь) и тогда все будет чики-пуки🙃"})
        vk.method("messages.send", {"user_id": id, "message": "Итак, чем я могу тебе помочь?", "keyboard": key['main_menu']})
    
    elif msg=="admin":
        vk.method("messages.send", {"user_id": id, "message": "Начинаю с начала:", "keyboard":key['start']})
    
    elif pay=="subscribe":
        vk.method("messages.send", {"user_id": id, "message": "Какие новости вы хотите получать?", "keyboard":key['subscribe']})
    
    elif pay=="enrollee":
        subscribe(type = 'SUB_E', id = id)
    
    elif pay=="schoolchild":
        subscribe(type = 'SUB_S', id = id)
    
    elif pay=="direction_selection":
        vk.method("messages.send", {"user_id": id, "message": "Как подобрать напрваление?", "keyboard":key['direction_selection']})
    
    elif pay=="sphere":
        data.set_field(connection = connection, table_name = "USERS", ID_VK = id, field = "SPHERE1", value = 0)
        data.set_field(connection = connection, table_name = "USERS", ID_VK = id, field = "SPHERE2", value = 0)
        data.set_field(connection = connection, table_name = "USERS", ID_VK = id, field = "SPHERE3", value = 0)
        vk.method("messages.send", {"user_id": id, "message": "Выберите сферу:", "keyboard":key['sphere']})
    
    elif pay=="Машиностроение" or pay=="Безопасность" or pay=="Энергетика" or pay=="IT-технологии" or pay=="Электроника" or pay=="Авиация" or pay=="Общество" or pay=="Экономика" or pay=="Химия" or pay=="Языки" or pay=="Физика":
        sphere_id = data.get_field(table_name = "SPHERE", connection = connection, select_field = 'SPHERE', field = 'NAME_SPHERE', value = pay)[0][0]
        sphere1 = data.get_field(table_name = "USERS", connection = connection, select_field = 'SPHERE1', field = 'ID_VK', value = id)[0][0]
        if sphere1==0:
            vk.method("messages.send", {"user_id": id, "message": "Сфера добавлена!", "keyboard":key['sphere']})
            data.set_field(connection = connection, table_name = 'USERS', ID_VK = id, field = 'SPHERE1', value = sphere_id)
        else:
            sphere2 = data.get_field(table_name = "USERS", connection = connection, select_field = 'SPHERE2', field = 'ID_VK', value = id)[0][0]
            if sphere2 == 0:
                vk.method("messages.send", {"user_id": id, "message": "Сфера добавлена!", "keyboard":key['sphere']})
                data.set_field(connection = connection, table_name = 'USERS', ID_VK = id, field = 'SPHERE2', value = sphere_id)
            else:
                sphere3 = data.get_field(table_name = "USERS", connection = connection, select_field = 'SPHERE3', field = 'ID_VK', value = id)[0][0]
                if sphere3 == 0:
                    vk.method("messages.send", {"user_id": id, "message": "Сфера добавлена!", "keyboard":key['sphere']})
                    data.set_field(connection = connection, table_name = 'USERS', ID_VK = id, field = 'SPHERE3', value = sphere_id)
                    search_direction(id)
        
   
    elif pay == "search":
        search_direction(id = id)
    
    elif pay == "lists":
        vk.method("messages.send", {"user_id": id, "message": "Выберите функцию:", "keyboard": key['list']})
    
    elif pay == "lk_code":
        pass
    
    elif pay == "frequency":
        vk.method("messages.send", {"user_id": id, "message": "Как часто вы хотите получать уведомления?", "keyboard": key['frequency']})

def get_msg():
    while True:
        #try:
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
        #except Exception:
            #print(2)
            #time.sleep(0.1)
                 
key = keyboards.get_keyboards() 

vk = auth()
print(vk)  
connection = data.connect()
print(connection)
get_msg()
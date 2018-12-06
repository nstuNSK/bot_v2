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

key = keyboards.get_keyboards()
vk = auth()
connection = data.connect()
def auth():
    token = getter.get_token()
    vk = vk_api.VkApi(token=token)
    vk._auth_token()
    return vk

def subscribe(type, id):
    if data.get_field(connection=connection, table_name="USERS",select_field = type, field="ID_VK", value=id)[0][0]==False:
        data.set_field(connection = connection, table_name = "USERS", ID_VK = id, field = type, value = "1")
        vk.method("messages.send", {"user_id": id, "message": "Теперь ты подписан на уведомления"})
    else:
        data.set_field(connection = connection, table_name = "USERS", ID_VK = id, field = type, value = "0")
        vk.method("messages.send", {"user_id": id, "message": "Теперь ты отписан от уведомлений"})
    #use_menu(status=data.get_field(connection=connection, table_name="USERS",select_field="status", field="ID_VK", value=id)[0][0])

def search_direction(id):
    res = []
    sphere = data.get_field(select_field = "SPHERE",table_name = "Status",connection= connection,value=id, field="id_vk")[0][0]
    if sphere == 0:
        vk.method("messages.send", {"user_id": id, "message": "Нет добавленных сфер:", "keyboard":keyboard_sphere})
    if sphere < 100:
        res = data.get_field(select_field = "DIRECTION, PROFILE_NAME, FACULT, DESCR, URL",table_name = "DIRECTIONS",connection= connection,value=sphere, field="SPHERE")
    elif sphere <10000:
        if int(sphere/100)>sphere%100:
            sphere = (sphere%100)*100+int(sphere/100)
        res = data.get_field(select_field = "DIRECTION, PROFILE_NAME, FACULT, DESCR, URL",table_name = "DIRECTIONS",connection= connection,value=sphere%100, field="SPHERE")
        temp = data.get_field(select_field = "DIRECTION, PROFILE_NAME, FACULT, DESCR, URL",table_name = "DIRECTIONS",connection= connection,value=int(sphere/100), field="SPHERE")
        if temp!=0:
            for item in temp:
                res.append(item)
        temp = data.get_field(select_field = "DIRECTION, PROFILE_NAME, FACULT, DESCR, URL",table_name = "DIRECTIONS",connection= connection,value=sphere, field="SPHERE")
        if temp!=0:
            for item in temp:
                res.append(item)
    else:
        a1 = int(sphere/10000)
        a2 = int(sphere/100)%100
        a3 = (sphere%10000)%100
        print("a1 = ",a1," a2 = ",a2," a3 = ",a3)
        print("id: ",sphere)
        if a1<a2 and a1<a3:
            sphere = a1*100
            if a2<a3:
                sphere = (sphere+a2)*100+a3
            else:
                sphere = (sphere+a3)*100+a2
        elif a2<a1 and a2<a3:
            sphere = a2*100
            if a1<a3:
                sphere = (sphere+a1)*100+a3
            else:
                sphere = (sphere+a3)*100+a1
        elif a3<a1 and a3<a2:
            sphere = a3*100
            if a2<a1:
                sphere = (sphere+a2)*100+a1
            else:
                sphere = (sphere+a1)*100+a2
        print("new id: ",sphere)
        res = data.get_field(select_field = "DIRECTION, PROFILE_NAME, FACULT, DESCR, URL",table_name = "DIRECTIONS",connection= connection,value=int(sphere/10000), field="SPHERE")
        temp = data.get_field(select_field = "DIRECTION, PROFILE_NAME, FACULT, DESCR, URL",table_name = "DIRECTIONS",connection= connection,value=sphere%100, field="SPHERE")
        if temp!=0:
            for item in temp:
                res.append(item)
        temp = data.get_field(select_field = "DIRECTION, PROFILE_NAME, FACULT, DESCR, URL",table_name = "DIRECTIONS",connection= connection,value=int(sphere/100), field="SPHERE")
        if temp!=0:
            for item in temp:
                res.append(item)
        temp = data.get_field(select_field = "DIRECTION, PROFILE_NAME, FACULT, DESCR, URL",table_name = "DIRECTIONS",connection= connection,value=sphere%10000, field="SPHERE")
        if temp!=0:
            for item in temp:
                res.append(item)
        temp = data.get_field(select_field = "DIRECTION, PROFILE_NAME, FACULT, DESCR, URL",table_name = "DIRECTIONS",connection= connection,value=int(str(sphere%100)+str(int(sphere/10000))), field="SPHERE")
        if temp!=0:
            for item in temp:
                res.append(item)
        temp = data.get_field(select_field = "DIRECTION, PROFILE_NAME, FACULT, DESCR, URL",table_name = "DIRECTIONS",connection= connection,value=int((sphere%100)/100), field="SPHERE")
        if temp!=0:
            for item in temp:
                res.append(item)
    response = ""
    vk.method("messages.send", {"user_id": id,"message":"По данным сферам найдены следуюшие направления:"})
    res = list(set(res))
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
    vk.method("messages.send", {"user_id": id,"message": response})
    vk.method("messages.send", {"user_id": id,"message": "Искал как в последний раз:)","keyboard": keyboard_default})


#WAIT_FILLING_POINTS = "-3"
#WAIT_FILLING = "-2"
#TEMP_FILLING = "-1"


def data_processing(id, pay, msg):
    if data.search_field(table_name="USERS",connection=connection,value=id, field="ID_VK")==False:
        data.set_user(table_name="USERS", connection=connection,ID_VK=id)
    
    if pay=={"command":"start"} or pay == "admin":
        vk.method("messages.send", {"user_id": id, "message": "Привет! Чем я могу тебе помочь?", "keyboard": key['main_menu']})
    
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
        sphere_id = data.get_field(table_name = "SPHERE", connection = connection, select_field = 'SPHERE', field = 'NAME_SPHERE', value = pay)
        sphere1 = data.get_field(table_name = "USERS", connection = connection, select_field = 'SPHERE1', field = 'ID_VK', value = id)

        if sphere1==0:
            data.set_field(connection = connection, table_name = 'USERS', ID_VK = id, field = 'SPHERE1', value = sphere_id)
        else:
            sphere2 = data.get_field(table_name = "USERS", connection = connection, select_field = 'SPHERE2', field = 'ID_VK', value = id)
            if sphere2 == 0:
                data.set_field(connection = connection, table_name = 'USERS', ID_VK = id, field = 'SPHERE2', value = sphere_id)
            else:
                sphere3 = data.get_field(table_name = "USERS", connection = connection, select_field = 'SPHERE3', field = 'ID_VK', value = id)
                if sphere3 == 0:
                    data.set_field(connection = connection, table_name = 'USERS', ID_VK = id, field = 'SPHERE3', value = sphere_id)
                else:
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
        except Exception:
            time.sleep(0.1)
        finally:
            data_processing(id=id, pay=pay, msg=msg)




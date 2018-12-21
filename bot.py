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
def from_pay_to_msg(pay):
    sql = "SELECT MSG FROM MSGS WHERE PAY = '"+str(pay)+"'"
    print(sql)
    return data.executeSQL(sql = sql, connection = connection)

def search_direction(id, type):
    if type == "SPHERE":
        sql = "SELECT NAME, DESCR, FACULTY, URL FROM DIRECTIONS WHERE ID IN (SELECT ID_DIR FROM DIR_SPHERES WHERE ID_SPHERE IN (SELECT ID_SPHERE FROM USERS_SPHERES WHERE ID_USER = "+str(id)+")) GROUP BY ID"
    elif type == "SUBJECTS":
        sql = "SELECT NAME, DESCR, FACULTY, URL FROM DIRECTIONS WHERE ID IN (SELECT ID_DIR FROM DIR_SUBJECTS WHERE ID_SUB IN (SELECT ID_SUB FROM USERS_SUBJECTS WHERE ID_USER = "+str(id)+")) GROUP BY ID"
    res = data.executeSQL(sql = sql, connection = connection)
    if res!=0:
        vk.method("messages.send", {"user_id": id,"message":random.choice(from_pay_to_msg("SEARCH_DIRECTION_START"))[0]})
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
        vk.method("messages.send", {"user_id": id,"message": random.choice(from_pay_to_msg("SEARCH_DIRECTION_END"))[0], 'keyboard': get_main_keyboard(id =id, connection = connection)})
    else:
        if type == "SPHERE":
            vk.method("messages.send", {"user_id": id,"message": random.choice(from_pay_to_msg("SEARCH_DIRECTION_ERROR"))[0], 'keyboard': key['sphere']})
        elif type == "SUBJECTS":
            vk.method("messages.send", {"user_id": id,"message":random.choice(from_pay_to_msg("SEARCH_DIRECTION_ERROR"))[0], 'keyboard': key['subjects']})

def add_sub(id, connection, sub):
    sql = "SELECT ID FROM SUBJECTS WHERE NAME = '"+str(sub)+"'"
    idSub = data.executeSQL(sql = sql, connection = connection)
    sql = "INSERT INTO USERS_SUBJECTS (ID_USER, ID_SUB) VALUES("+str(id)+", "+str(idSub[0][0])+")"
    data.executeSQL(sql = sql, connection = connection)

def add_sphere(id, connection, pay):
    sql = "SELECT ID FROM SPHERES WHERE NAME = '"+str(pay)+"'"
    idSph = data.executeSQL(sql = sql, connection = connection)
    sql = "INSERT INTO USERS_SPHERES (ID_USER, ID_SPHERE) VALUES("+str(id)+", "+str(idSph[0][0])+")"
    data.executeSQL(sql = sql, connection = connection)

def get_main_keyboard(id, connection):
    sql = "SELECT SUBSCRIBE FROM USERS WHERE ID = "+str(id)
    res = data.executeSQL(sql = sql, connection = connection)
    if res[0][0] == True:
        return key['main_menu_on']
    else:
        return key['main_menu_off']

def data_processing(id, pay, msg):
    if data.search_field(table_name="USERS",connection=connection,value=id, field="ID")==False:
        data.set_user(table_name="USERS", connection=connection,ID_VK=id)
    
    if pay=={"command":"start"} or pay == "admin":
        vk.method("messages.send", {"user_id": id, "message": random.choice(from_pay_to_msg("START"))[0]})
        vk.method("messages.send", {"user_id": id, "message": random.choice(from_pay_to_msg("HELP_MSG"))[0], "keyboard": get_main_keyboard(id =id, connection = connection)})
    
    elif msg=="admin":
        vk.method("messages.send", {"user_id": id, "message": random.choice(from_pay_to_msg("ADMIN"))[0], "keyboard":key['start']})
    
    elif pay == "main_menu":
        vk.method("messages.send", {"user_id": id, "message": random.choice(from_pay_to_msg("MAIN_MENU"))[0], "keyboard":get_main_keyboard(id =id, connection = connection)})

    elif pay=="subscribe":
        if data.get_field(connection=connection, table_name="USERS",select_field = "SUBSCRIBE", field="ID", value=id)[0][0]==False:
            print("tut")
            data.set_field(connection = connection, table_name = "USERS", ID_VK = id, field = "SUBSCRIBE", value = 1)
            vk.method("messages.send", {"user_id": id, "message": random.choice(from_pay_to_msg("SUBSCRIBE"))[0], 'keyboard': get_main_keyboard(id =id, connection = connection)})
        else:
            data.set_field(connection = connection, table_name = "USERS", ID_VK = id, field = "SUBSCRIBE", value = 0)
            vk.method("messages.send", {"user_id": id, "message": random.choice(from_pay_to_msg("UNSUBSCRIBE"))[0], 'keyboard': get_main_keyboard(id =id, connection = connection)})
    
    elif pay=="direction_selection":
        vk.method("messages.send", {"user_id": id, "message": random.choice(from_pay_to_msg("DIRECTION_SELECTION"))[0], "keyboard":key['direction_selection']})
    
    elif pay=="sphere":
        sql = "DELETE FROM USERS_SPHERES WHERE ID_USER = "+str(id)
        data.executeSQL(sql = sql, connection = connection)
        vk.method("messages.send", {"user_id": id, "message": random.choice(from_pay_to_msg("SPHERE"))[0], "keyboard":key['sphere']})
    
    elif pay=="Машиностроение" or pay=="Безопасность" or pay=="Энергетика" or pay=="IT-технологии" or pay=="Электроника" or pay=="Авиация" or pay=="Общество" or pay=="Экономика" or pay=="Химия" or pay=="Языки" or pay=="Физика":
        sql = "SELECT ID_SPHERE FROM USERS_SPHERES WHERE ID_USER = "+str(id)
        size = data.executeSQL(sql = sql, connection = connection)
        if size!=0:
            if len(size) < 3:
                add_sphere(id=id,connection=connection, pay = pay)
                vk.method("messages.send", {"user_id": id, "message": random.choice(from_pay_to_msg("ADD_MSG"))[0], "keyboard":key['sphere']})
                if len(size)+1>=3:
                    search_direction(id = id, type = "SPHERE")
        else:
            add_sphere(id=id,connection=connection, pay = pay)
            vk.method("messages.send", {"user_id": id, "message": random.choice(from_pay_to_msg("ADD_MSG"))[0], "keyboard":key['sphere']})
        
   
    elif pay=="name_dir":
        sql = "DELETE FROM USERS_SUBJECTS WHERE ID_USER = "+str(id)
        data.executeSQL(sql=sql, connection=connection)
        vk.method("messages.send", {"user_id": id, "message": random.choice(from_pay_to_msg("NAME_DIR"))[0], "keyboard":key['subjects']})

    elif pay == "math" or pay == "biology" or pay == "geography" or pay == "foreign_language" or pay == "informatics" or pay == "history" or pay == "literature" or pay == "social_science" or pay == "physics" or pay == "chemistry":
        sql = "SELECT ID_SUB FROM USERS_SUBJECTS WHERE ID_USER = "+str(id)
        idSub = data.executeSQL(sql = sql, connection = connection)
        if idSub !=0:
            if len(idSub)<2:
                add_sub(id = id, connection = connection, sub = pay)
                vk.method("messages.send", {"user_id": id, "message": random.choice(from_pay_to_msg("ADD_MSG"))[0], "keyboard":key['subjects']})
                if(len(idSub)+1>=2):
                    search_direction(id = id, type = "SUBJECTS")
        else:
            add_sub(id = id, connection = connection, sub = pay)
            vk.method("messages.send", {"user_id": id, "message": random.choice(from_pay_to_msg("ADD_MSG"))[0], "keyboard":key['subjects']})
    
    elif pay == "search_by_sphere":
        search_direction(id = id, type = "SPHERE")
    elif pay == "search_by_subjects":
        search_direction(id = id, type = "SUBJECTS")
    elif pay == "lists":
        vk.method("messages.send", {"user_id": id, "message": "Выберите функцию:", "keyboard": key['list']})
    
    elif pay == "lk_code":
        vk.method("messages.send", {"user_id": id, "message": "Меня пока что этому не научили😞\nНо совсем скоро научат, обещаю!", "keyboard": get_main_keyboard(id =id, connection = connection)})
    
    elif pay == "frequency":
        vk.method("messages.send", {"user_id": id, "message": "Меня пока что этому не научили😞\nНо совсем скоро научат, обещаю!", "keyboard": get_main_keyboard(id =id, connection = connection)})
    
    elif msg == "Бу!":
        vk.method("messages.send", {"user_id": id, "message": random.choice(from_pay_to_msg("FEAR_MSG"))[0], "keyboard": get_main_keyboard(id =id, connection = connection)})
    else:
        vk.method("messages.send", {"user_id": id, "message": random.choice(from_pay_to_msg("ERROR"))[0], "keyboard": get_main_keyboard(id =id, connection = connection)})

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
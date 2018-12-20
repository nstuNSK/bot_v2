import requests
import pymysql.cursors
import json
import getter
def connect():
    #try:
        user = getter.get_user()
        password = getter.get_password()
        cnx = pymysql.connect(
            user=user,
			password = password,
            host = 'localhost',
            db='TEMP'
        )
        return cnx
connection = connect()
subjects = {'Математика': "math",
'Биология': "biology",
'История': "history",
'Иностранный язык': "foreign_language",
'Литература': "literature",
'Информатика': "informatics",
'География': "geography",
'Физика': "physics",
'Химия': "chemistry",
'Обществознание': "social_science",
'Иностр. яз.': "foreign_language"}

def get_field(table_name,field1, field2, value):
    with connection.cursor() as cursor:
        sql = "SELECT " + field1 + " FROM " + table_name + " WHERE " + field2 + " = %s"
        print(sql)
        cursor.execute(sql,(value))
        return list(cursor.fetchone())[0]

def search_field(table_name, field, value):
    if value != None:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM "+table_name+" WHERE + " + str(field) + " = " + str(value)
            s = cursor.execute(sql)
            if s==0:
                return False
            else:
                return True
    else:
        return True


def set_dir(values):
    if values["BALL_K"] == None:
        values["BALL_K"] = 0
    if values["BALL_B"] == None:
        values["BALL_B"] = 0
    if values["DESCR"] == None:
        values["DESCR"] = "null"
    if values["PROFILE_NAME"]==None:
        values["PROFILE_NAME"] = "null"
    with connection.cursor() as cursor:
            if search_field("DIRECTIONS", "ID", values["ID"]) == False:
                sql = "INSERT INTO DIRECTIONS (DESCR, PROFILE_NAME, ID, FACULTY, KEYS_PLUS, NAME, BALL_K, BALL_B, URL) VALUES ( '" +str(values["DESCR"])+ "', '"+str(values["DESCR"])+"', '"+str(values["ID"])+"', '"+str(values["FACULT"])+"', '"+str(values["KEYS_PLUS"])+"', '"+str(values["DIRECTION"])+"', '"+str(values["BALL_K"])+"', '"+str(values["BALL_B"])+"', '"+str(values["URL"])+"')"
                cursor.execute(sql)
                connection.commit()

def executeSQL(sql):
    with connection.cursor() as cursor:
        res = cursor.execute(sql)
        connection.commit()
        if res!=0:
            return list(cursor.fetchall())
        else:
            return 0


def set_dir_sph(values):
    with connection.cursor() as cursor:
        sql = "INSERT INTO DIR_SPHERES (ID_DIR, ID_SPHERE) VALUES"
        size = len(sql)
        for sphere in values["data"]:
            if sphere["SPHERE"]!=None:
                sql2 = "SELECT * FROM SPHERES WHERE NAME = '"+str(sphere["SPHERE"])+"'"
                sph = executeSQL(sql2)
                sql = sql+"("+str(values["ID"])+", "+str(sph[0][0])+"),
        if size < len(sql):
            sql = sql[0:len(sql)-1]
            print(sql)
            cursor.execute(sql)
            connection.commit()

def set_dir_sub(values):
    disk2 = values["DISC2"]
    disk3 = values["DISC3"]
    d2 = subjects[disk2]
    d3 = subjects[disk3]
    sql = "SELECT ID FROM SUBJECTS WHERE NAME = '"+str(d2)+"'"
    r = executeSQL(sql)
    sql = "INSERT INTO DIR_SUBJECTS (ID_DIR, ID_SUB) VALUES("+str(values["ID"])+", "+str(r[0][0])+")"
    executeSQL(sql)
    sql = "SELECT ID FROM SUBJECTS WHERE NAME = '"+str(d3)+"'"
    r = executeSQL(sql)
    sql = "INSERT INTO DIR_SUBJECTS (ID_DIR, ID_SUB) VALUES("+str(values["ID"])+", "+str(r[0][0])+")"
    executeSQL(sql)




def main():
    url = getter.get_nstu_url()
    html = requests.get(url)
    text = html.text
    text = bytes(text, 'utf-8').decode('unicode-escape')
    api = json.loads(text)
    for item in api:
        set_dir(item)
    for item in api:
        set_dir_sub(item)
        set_dir_sph(item)

if __name__== '__main__':
    main()

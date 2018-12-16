import pymysql.cursors
import getter

def connect():
    #try:
        user = getter.get_user()
        password = getter.get_password()
        cnx = pymysql.connect(
            user=user,
			password = password,
            host = 'localhost',
            db='DATA'
        )
        return cnx

def set_user(table_name,connection,ID_VK):
    if search_field(table_name, connection, ID_VK , "ID")==False:
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO " + table_name + " (ID, LAST_NEWS) VALUES (%s, '2017-01-01 00:00:00')"
                print(sql)
                cursor.execute(sql,(ID_VK))
                connection.commit()
                return True
        except:
            return False
    else:
         return False

def search_field(table_name,connection,value, field):
        with connection.cursor() as cursor:
            sql = "SELECT * FROM " + table_name + " WHERE " + field + " = %s"
            str = cursor.execute(sql,(value))
            if str==0:
                return False
            else:
                return True

def get_field(connection,table_name,select_field,field,value):
        with connection.cursor() as cursor:
            #print("Ищу: ",value)
            sql = "SELECT " + select_field + " FROM " + table_name + " WHERE " + field + " = %s"
            size = cursor.execute(sql,(value))
            #print("Нашел: ",size, " значений")
            if size == 0:
                return 0
            return list(cursor.fetchall())
            #return cursor.fetchall()

def set_complex_str_in_field(connection, table_name, ID_VK, field, value):
    with connection.cursor() as cursor:
        sql = "UPDATE " + table_name + " SET " + field + " = " +"'"+str(value)+"'"+ " WHERE ID_VK = %s"
        r = cursor.execute(sql, (ID_VK))
        connection.commit()

def set_field(connection, table_name, ID_VK, field, value):
    with connection.cursor() as cursor:
        sql = "UPDATE " + table_name + " SET " + field + " = " + str(value) + " WHERE ID_VK = %s"
        r = cursor.execute(sql, (ID_VK))
        connection.commit()
def get_fields(connection,table_name,select_field,field,value):
    with connection.cursor() as cursor:
            sql = "SELECT " + select_field + " FROM " + table_name + " WHERE " + field + " = %s"
            cursor.execute(sql,(value))
            return list(cursor.fetchone())

def executeSQL(sql, connection):
    with connection.cursor() as cursor:
        res = cursor.execute(sql)
        connection.commit()
        if res!=0:
            return list(cursor.fetchall())
        else:
            return 0

#def get_field(connection, table_name, ID_VK, field):
#    with connection.cursor() as cursor:
#        sql = "SELECT " + field + " FROM " + table_name + " WHERE id_vk = %s"
#        cursor.execute(sql,(ID_VK))
#        return list(cursor.fetchone())[0]

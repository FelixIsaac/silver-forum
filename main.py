#!/usr/bin/python3
from ast import Bytes
import sqlite3,re,base64,os
import scrypt
#h1 = 
global cursor,conn
conn = sqlite3.connect('login.db')
cursor = conn.cursor()
if not cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()==[('USERS',)]:
    conn.execute('''CREATE TABLE USERS
             (USERNAME       TEXT    NOT NULL,
             PASSWORD       INT     NOT NULL,
             EMAIL          TEXT    NOT NULL);
            ''')
    conn.commit()
    
def hash_password(password):
    return base64.b64encode(scrypt.encrypt(os.urandom(64), password, maxtime=0.5)).decode()

def verify(username, password):
    result=lookup(username)
    cursor.execute("""SELECT PASSWORD FROM "users" WHERE "username" = "%s";"""%(username))
    temp=cursor.fetchone()
    if temp:
        for i in temp:
            hashed_password=i
            break
    hashed_password=base64.b64decode(hashed_password)
    print(hashed_password)
    try:
        scrypt.decrypt(hashed_password, password, maxtime=0.5)
        return True
    except scrypt.error:
        return False

def lookup(username):
    cursor.execute("""SELECT * FROM "users" WHERE "username" = "%s";"""%(username))
    result = cursor.fetchone()
    return result

def validate(username,password,email):
    if not (20>=len(username) and 3<=len(username)):
        return [False,"Usernames cannot be longer than 20 character or shorter than 3 characters."]
    if not re.match("^[a-zA-Z0-9_]*$",username):
        return [False,"Username cannot contain special characters."]
    if '\t' in username or '\n' in username or '\r' in username or '\f' in username:
        return [False,"Username cannot contain characters like newlines or tabs."]
    if not isinstance(username,str):
        return [False,"Username cannot contain unicode."]
    if not isinstance(password,str):
        return [False,"Passwords cannot contain unicode."]
    if not 8<len(password):
        return [False,"Passwords must be longer than 8 characters"]
    if not re.search("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)",email):
        return [False,"Invalid Email address."]
    if lookup(username):
        return [False,"Username or Email already exist."]
    return [True,""]

def add(username,password,email):
    #result=validate(username,password,email)
    result=[True]
    if result[0]:
        cursor.execute("""INSERT INTO USERS (USERNAME,PASSWORD,EMAIL) VALUES ("%s","%s","%s");"""%(username,hash_password(password),email))
        conn.commit()
    else:
        print('ERORR:',result[1])

def delete(username):
    cursor.execute("""INSERT INTO USERS (USERNAME,PASSWORD,EMAIL) VALUES ("%s","%s","%s");"""%(username))
    conn.commit()

add('ewe','123456789','ee@a.com')
print(lookup('ewe'))
print(verify('ewe','123456789'))
conn.close()
#for name in cursor.execute('select * from "users" where "username" = "paul";'):
#    print(name)

#conn.close()
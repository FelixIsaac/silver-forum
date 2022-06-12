#!/usr/bin/python3
#IT NEEDS THE GOD DAMN POSTGRES SERVER TO RUN THE FILE IS RIGHT THERE JUST READ IT AHHHHHHHHHHHHH
import psycopg2,re,base64,os,string,random
import scrypt


global cursor,conn
conn = psycopg2.connect(
    host="localhost",
    database="login",
    user="postgres",
    password="postgres")
cursor = conn.cursor()
try:
    cursor.execute("""SELECT EXISTS (
    SELECT FROM 
        pg_tables
    WHERE 
        schemaname = 'public' AND 
        tablename  = 'login'
    );
    """)
    print('yes')
except:
    print('no')
    conn.rollback()
    cursor.execute('''
    CREATE TABLE USERS (
        ISADMIN       INTEGER     NOT NULL,
        USERNAME       TEXT    NOT NULL,
        PASSWORD       TEXT     NOT NULL,
        EMAIL          TEXT    NOT NULL
             );
            ''')
    conn.commit()
 
def hash_password(password):
    temp=scrypt.encrypt("".join(random.choices(string.ascii_letters+string.digits+string.punctuation,k=256)), password, maxtime=0.5)
    #print(temp)
    type(temp)
    return base64.b64encode(temp).decode()

def verify(username, password):
    result=lookup(username)
    if result:
        cursor.execute("""SELECT PASSWORD FROM "users" WHERE "username" = "%s";"""%(username))
        temp=cursor.fetchone()
        if temp:
            for i in temp:
                hashed_password=i
                break
        #print(hashed_password)
        hashed_password=base64.b64decode(hashed_password)
        #print(hashed_password)
        try:
            scrypt.decrypt(hashed_password, password, 0.5)
            return True
        except scrypt.error:
            return False
    else:
        return False

def lookup(username):
    try:
        cursor.execute("""SELECT * FROM users WHERE USERNAME = "%s";"""%(username))
        result = cursor.fetchone()
        return result
    except:
        conn.rollback()
        return False

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

def add(isadmin,username,password,email):
    result=validate(username,password,email)
    #result=[True]
    if result[0]:
        temp=hash_password(password)
        #print(temp)
        if isadmin==1:
            cursor.execute("""INSERT INTO USERS (ISADMIN,USERNAME,PASSWORD,EMAIL) VALUES ("%s","%s","%s","%s");"""%(0,username,temp,email))
        conn.commit()
        print('done')
    else:
        print('ERORR:',result[1])

def delete(username):
    cursor.execute("""DELETE FROM USERS WHERE USERNAME = "%s";"""%(username))
    conn.commit()

add(0,'ewe','123456789','ee@a.com')

#tests for username
add(0,'ee','123456789','ee@aaa.com')
#tests for password
add(0,'eaa','12345678','ee@aaa.com')
#test for email
add(0,'esa','123456789','eeaaa.com')

print(lookup('ewe'))

if verify('ewe','123456789'):
    print('corect password')
else:
    print('wrong password')

if verify('ewe','123456789000000000'):
    print('corect password')
else:
    print('wrong password')


conn.close()
#for name in cursor.execute('select * from "users" where "username" = "paul";'):
#    print(name)

#conn.close()
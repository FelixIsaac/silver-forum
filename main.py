#!/usr/bin/python3
import sqlite3,os
import scrypt
h1 = scrypt.hash('password', 'random salt')
os.remove('test.db')
conn = sqlite3.connect('test.db')
conn.execute('''CREATE TABLE USERS
         (ID INT PRIMARY KEY    NOT NULL,
         USERNAME       TEXT    NOT NULL,
         PASSWORD       INT     NOT NULL,
         EMAIL          TEXT    NOT NULL)
        ''')
conn.execute("INSERT INTO USERS (ID,USERNAME,PASSWORD,EMAIL) VALUES (1, 'Paul', 32,'GG@gmail.com')");
conn.commit()

mycursor = conn.cursor()
for dname in mycursor.execute('SELECT * FROM "USERS" WHERE "USERNAME" = "Paul"'):
    print(name)

#conn.close()
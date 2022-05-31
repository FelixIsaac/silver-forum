#!/usr/bin/python3

from datetime import date
import sqlite3
import re
from argon2 import PasswordHasher

conn = sqlite3.connect('login.db')
cursor = conn.cursor()
ph = PasswordHasher()

# Create "users" table
# Todo: Switch to PostgreSQL, and move initialisation to .SQL file
if not cursor.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall() == [('USERS',)]:
    conn.execute('''
        CREATE TABLE USERS (
            ID             INTEGER PRIMARY KEY,
            USERNAME       TEXT    UNIQUE NOT NULL,
            PASSWORD       INT     NOT NULL,
            EMAIL          TEXT    UNIQUE NOT NULL,
            ADMIN          INT     DEFAULT 0 NOT NULL,
            GENDER         TEXT    NOT NULL,
            BIRTH_YEAR     INT     NOT NULL
        );
    ''')

    conn.commit()


def lookup(username):
    cursor.execute(
        "SELECT * FROM users WHERE username = ?",
        (username,)
    )

    return cursor.fetchone()


def verify(username, password):
    user = lookup(username)
    return ph.verify(user[1], password)


# Username standards are under https://www.rfc-editor.org/rfc/rfc5321#section-4.5.3
def validate(username, password, email, birth_year):
    if date.today().year - birth_year > 12:
        return [False, "Sorry, you have to at least 13 years old to register."]

    if not (50 >= len(username) and 3 <= len(username)):
        return [False, "Usernames cannot be longer than 50 characters or shorter than 3 characters."]

    if not re.match("^[a-zA-Z0-9_]*$", username):
        return [False, "Username cannot contain special characters."]

    if '\t' in username or '\n' in username or '\r' in username or '\f' in username:
        return [False, "Username cannot contain characters like newlines or tabs."]

    if not isinstance(username, str):
        return [False, "Username cannot contain special characters."]

    if not isinstance(password, str):
        return [False, "Passwords cannot contain special characters."]

    if not 8 < len(password):
        return [False, "Passwords must be longer than 8 characters"]

    if not re.search("(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
        return [False, "Invalid Email address."]

    if lookup(username):
        return [False, "Username or Email already exist."]

    return [True, ""]


def add(username, password, email, gender, birth_year):
    username = username.strip()
    password = password.strip()
    email = email.lower().strip()

    result = validate(username, password, email, birth_year)

    if result[0]:
        hashed_password = ph.hash(password)

        cursor.execute(
            "INSERT INTO USERS (USERNAME, PASSWORD, EMAIL) VALUES (?, ?, ?);",
            (username, hashed_password, email)
        )

        conn.commit()

        return [True, "Added user record"]
    else:
        print('ERROR:', result[1])
        return result[1]


def delete(username, password):
    if verify(username, password):
        cursor.execute("DELETE FROM users WHERE username = ?;", (username))
        conn.commit()


conn.close()

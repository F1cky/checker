import sqlite3
import telebot
import config
import requests
from config import db, TOKEN
def first_join(user_id, username):
    connection = sqlite3.connect(db)
    q = connection.cursor()
    q = q.execute('SELECT * FROM users WHERE user_id IS '+str(user_id))
    row = q.fetchone()
    if row is None:
        q.execute("INSERT INTO users (user_id,  nick) VALUES ('%s', '%s')"%(user_id,username))
        connection.commit()
    connection.close()
def admin_message(text):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    cursor.execute(f'SELECT user_id FROM users')
    row = cursor.fetchall()
    return row
    conn.close()

def stats():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    row = cursor.execute(f'SELECT user_id FROM users').fetchone()
    amount_user_all = 0
    while row is not None:
        amount_user_all += 1
        row = cursor.fetchone()
    msg = '❕ Информация:\n\n❕ Пользователей в боте - ' + str(amount_user_all)
    return msg
    conn.close()


def stats_users():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    ra = cursor.execute(f'SELECT user_id FROM users').fetchone()
    amount_user_all = 0
    while ra is not None:
        amount_user_all += 1
        ra = cursor.fetchone()
    mkl = str(amount_user_all)
    return mkl
    conn.close()

def checking():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    ro = cursor.execute(f'SELECT all_ch FROM chek').fetchone()
    all_checking = 0
    while ro is not None:
        all_checking += 1
        ro = cursor.fetchone()
    mbn = str(all_checking)
    return mbn
    conn.close()

def check():
    conn = sqlite3.connect(db)
    cursor = conn.cursor()
    rn = cursor.execute(f"SELECT all_ch FROM chek").fetchone()
    all_check = 0
    while rn is not None:
        all_check += 1
        rn = cursor.fetchone()
    mcv = str(all_check)
    cursor.execute(f'INSERT INTO chek (all_ch) VALUES (?)', (mcv,))
    conn.commit()
    conn.close()

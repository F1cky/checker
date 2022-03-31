import requests
from requests import get, post
from telebot import types
from telebot import util
from datetime import datetime
import telebot
import execute
import cursor
from bs4 import BeautifulSoup
import random
from random import randint
import ctypes
import colorama
from colorama import Fore, init
import click
import os
from config import TOKEN, admin
import keyboard as kb
import functions as func
import json
import sqlite3
import time
import urllib
import urllib.request
import re
import traceback
import config
import datetime

bot = telebot.TeleBot(TOKEN)
bot_username = bot.get_me().username

# Запись в Базу Данных
@bot.message_handler(commands=['start'])
def start(message: types.Message):
    chat_id = message.chat.id
    username = message.from_user.username    
    if message.from_user.username == None:
        bot.send_message(chat_id, ' Вам необходимо установить логин для работы с ботом!')
    else:
        func.first_join(user_id=chat_id, username=username)
        bot.send_message(chat_id, '*Добро пожаловать, {}!*\n\n*Discord Liquid* — бесплатный чекер токенов Discord, который позволи тебе проверить все свои токены в пару кликов, не скачивая лишних приложений на свой компьютер!'.format(message.from_user.first_name), parse_mode="Markdown", reply_markup=kb.menu)

@bot.message_handler(commands=['admin'])
def start(message: types.Message):
    if message.chat.id == admin:
        bot.send_message(message.chat.id, ' {}, вы авторизованы!'.format(message.from_user.first_name),
                         reply_markup=kb.admin)
#Функции бота
@bot.callback_query_handler(func=lambda call: True)        
def handler_call(call):
    chat_id = call.message.chat.id
    message_id = call.message.message_id
    if call.data == 'statistics':
        bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=func.stats(), reply_markup=kb.admin)
    elif call.data == 'message':
        msg = bot.send_message(chat_id=chat_id, text='Введите текст для рассылки.\n\nДля отмены напишите "-" без кавычек!')
        bot.register_next_step_handler(msg, message1)
    elif call.data == 'menu':
        bot.send_message(message.chat.id, 'Операция отменена.')

def message1(message):
    text = message.text
    if message.text.startswith('-'):
        bot.send_message(message.chat.id, 'Операция отменена.')
    else:
        info = func.admin_message(text)
        bot.send_message(message.chat.id, text='✅ Рассылка начата!')
        for i in range(len(info)):
            try:
                time.sleep(1)
                bot.send_message(info[i][0], str(text))
            except:
                pass
        bot.send_message(message.chat.id, text='✅ Рассылка завершена!')
        print (info)

@bot.message_handler(content_types=['text'])
def bot_message(message):     
    if message.chat.type == 'private':
        if message.text == '❗️ Инфо':
            bot.send_message(message.chat.id, '<b>DISCORD LIQUID — удобный бот для чека Ваших токенов Discord!</b>\n\n<b>Мы умеем делать для тебя все это:</b>\n— чек на валидные токены с верификацией\n— чек на токены с активной подпиской\n— чек на токены с платежными способами\n— чек на неверифицированные токены\n— автоматически удаляет дубликаты\n\n<b>Администратор сервиса:</b> @FickyXXL\n<b>Тех. поддержка:</b> @FickyXXL', parse_mode="html")

        elif message.text == '📥 Прочекать токены':
            msg = bot.send_message(message.chat.id, 'Необходимо прислать мне .txt файл с Вашими токенами!\n\n📩<code>Принимаем только файлы с расширением .txt!</code>', parse_mode="html", reply_markup=kb.naz)
            bot.register_next_step_handler(msg, user_tokens)

        elif message.text == '📊 Статистика':
            bot.send_message(message.chat.id, f'<b>Статистика нашего сервиса</b>\nПользователей сервиса: {func.stats_users()} человек(а)\nКоличество чеков: {func.checking()} раз(а)', parse_mode="html")

        elif message.text == '🔐 Доступ':
            bot.send_message(message.chat.id, f'<code>Пока что бот будет бесплатный, а когда я сделаю много функций будет стоить 50₽ в месяц</code>', parse_mode="html")

@bot.message_handler(commands=["application"])
def user_tokens(message):
    if message.chat.type == 'private':
        if message.text == 'Назад':
            bot.send_message(message.chat.id, 'Привет, <b>{}</b>!\nДобро пожаловать в чекер токенов Discord'.format(message.from_user.first_name), reply_markup = kb.menu, parse_mode="html")
        
        elif message.content_type == 'document':           
            func.check()

            try:
                chat_id = message.chat.id

                ib = random.randint(1, 10000)
                q = 0
                g = 0
                v = 0
                m = 0 
                h = 0

                cards = 0
                full = 0

                idlist = []


                dirPath = f'C:/Program Files (x86)/users/{chat_id}'

                if not os.path.isdir(dirPath): 
                    os.mkdir(dirPath) 
                else: 
                    pass


                file_info = bot.get_file(message.document.file_id, )
                downloaded_file = bot.download_file(file_info.file_path)

                src = f'{dirPath}/tokens.txt';
                with open(src, 'wb') as new_file:
                    new_file.write(downloaded_file)

                bot.reply_to(message, "Токены приняты в обработку. Ожидайте...", reply_markup = kb.menu)

                tic = time.perf_counter()

                input_file = f"{dirPath}/tokens.txt"
                with open(input_file, "r") as fp:
                    lines = fp.readlines()
                    new_lines = []
                    for line in lines:
                        #- Strip white spaces
                        line = line.strip()
                        if line not in new_lines:
                            new_lines.append(line)

                output_file = f"{dirPath}/output.txt"
                with open(output_file, "w") as fp:
                    fp.write("\n".join(new_lines))

                with open(f'{dirPath}/output.txt') as f:
                    text = f.read()
                    nodyb = text.count('\n') + 1

                bot.send_message(message.chat.id, f"При загрузке все дубли были удалены.")

                with open(f"{dirPath}/output.txt","r+") as f:
                    for line in f:
                        token=line.strip("\n")
                        json = requests.get("https://discordapp.com/api/v9/users/@me/library", headers={"authorization": token})
                        if json.status_code == 200:
                            jsonn = requests.get(f"https://discordapp.com/api/v9/users/@me?verified", headers={"authorization": token})
                            json_response = jsonn.json()
                            if json_response["id"] not in idlist:
                                idlist.append(json_response["id"])
                                q += 1

                                file4 = open(f"{dirPath}/Valid.txt", "a")
                                file4.write(f"{token}\n")
                                file4.close()

                                if json_response["phone"] == None:
                                    v += 1

                                    file12 = open(f"{dirPath}/Notverified.txt", "a")
                                    file12.write(f"{token}\n")
                                    file12.close()

                                else:
                                    m += 1

                                    file13 = open(f"{dirPath}/Verified.txt", "a")
                                    file13.write(f"{token}\n")
                                    file13.close()
                            else:
                                h += 1
            
                        else:
                            g += 1

                            file3 = open(f"{dirPath}/Invalid.txt", "a")
                            file3.write(f"{token}\n")
                            file3.close()

                if os.path.isfile(f'{dirPath}/Valid.txt'):
                    with open(f"{dirPath}/Valid.txt","r+") as f:
                        for line in f:
                            token=line.strip("\n")
                            for json in requests.get("https://discordapp.com/api/v7/users/@me/billing/payment-sources", headers={"authorization": token}).json():
                                try:               
                                    if json["type"] == 1:

                                        file1 = open(f"{dirPath}/nodybcard.txt", "a")
                                        file1.write(f"{token}\n")
                                        file1.close()
                                    
                                        input_file = f"{dirPath}/nodybcard.txt"
                                        file5 = open(input_file, "r")
                                        with file5 as fp:
                                            lines = fp.readlines()
                                            new_lines = []
                                            for line in lines:
                                                line = line.strip()
                                                if line not in new_lines:
                                                    new_lines.append(line)
                                        file5.close()

                                        output_file = f"{dirPath}/Cards.txt"
                                        with open(output_file, "w") as fp:
                                            fp.write("\n".join(new_lines))

                                        with open(f'{dirPath}/Cards.txt') as f:
                                            text = f.read()
                                            cards = text.count('\n') + 1

                                    else:

                                        file2 = open(f"{dirPath}/nodybcard.txt", "a")
                                        file2.write(f"{token}\n")
                                        file2.close()
                                
                                        input_file = f"{dirPath}/nodybcard.txt"
                                        file5 = open(input_file, "r")
                                        with file5 as fp:
                                            lines = fp.readlines()
                                            new_lines = []
                                            for line in lines:
                                                line = line.strip()
                                                if line not in new_lines:
                                                    new_lines.append(line)
                                        file5.close()

                                        output_file = f"{dirPath}/Cards.txt"
                                        with open(output_file, "w") as fp:
                                            fp.write("\n".join(new_lines))

                                        with open(f'{dirPath}/Cards.txt') as f:
                                            text = f.read()
                                            cards = text.count('\n') + 1
                                except:
                                    pass

                    with open(f"{dirPath}/Valid.txt","r+") as f:
                        for line in f:
                            token=line.strip("\n")
                            for json in requests.get("https://discord.com/api/v7/users/@me/billing/subscriptions", headers={"authorization": token}).json():
                                try:
                                    if json['items'][0]['plan_id'] == "511651880837840896":
                                        full += 1

                                        file14 = open(f"{dirPath}/Nitro.txt", "a")
                                        file14.write(f"{token}\n")
                                        file14.close()

                                    else:
                                        pass
                                
                                except:
                                    pass                      

                if os.path.isfile(f'{dirPath}/Valid.txt'):
                    bot.send_document(chat_id=chat_id, document=open(f'{dirPath}/Valid.txt', 'rb'))
                    os.remove(f'{dirPath}/Valid.txt')

                if os.path.isfile(f'{dirPath}/Invalid.txt'):
                    bot.send_document(chat_id=chat_id, document=open(f'{dirPath}/Invalid.txt', 'rb'))
                    os.remove(f'{dirPath}/Invalid.txt')

                if os.path.isfile(f'{dirPath}/Notverified.txt'):
                    bot.send_document(chat_id=chat_id, document=open(f'{dirPath}/Notverified.txt', 'rb'))
                    os.remove(f'{dirPath}/Notverified.txt')

                if os.path.isfile(f'{dirPath}/Verified.txt'):
                    bot.send_document(chat_id=chat_id, document=open(f'{dirPath}/Verified.txt', 'rb'))
                    os.remove(f'{dirPath}/Verified.txt')

                if os.path.isfile(f'{dirPath}/nodybcard.txt'):
                    bot.send_document(chat_id=chat_id, document=open(f'{dirPath}/nodybcard.txt', 'rb'))
                    os.remove(f'{dirPath}/nodybcard.txt')

                if os.path.isfile(f'{dirPath}/Cards.txt'):
                    bot.send_document(chat_id=chat_id, document=open(f'{dirPath}/Cards.txt', 'rb'))
                    os.remove(f'{dirPath}/Cards.txt')

                if os.path.isfile(f'{dirPath}/Nitro.txt'):
                    bot.send_document(chat_id=chat_id, document=open(f'{dirPath}/Nitro.txt', 'rb'))
                    os.remove(f'{dirPath}/Nitro.txt')

                os.remove(f'{dirPath}/output.txt')
                os.remove(f'{dirPath}/tokens.txt')

                toc = time.perf_counter()

                bot.send_message(message.chat.id, f"✨ <b>Токены были успешно проверены!</b>\n<b>Valid:</b> {q}\n<b>Invalid:</b> {g}\n<b>Всего токенов:</b> {nodyb}\n\n<b>С вериф номерами:</b> {m}\n<b>Без вериф номеров:</b> {v}\n\n<b>С картами:</b> {cards}\n<b>С нитро:</b> {full}\n\nВремя на чек: {toc - tic:0.2f} сек.", parse_mode="html")

            except Exception as e:
                bot.reply_to(message, e)

# Поддержание работы
bot.infinity_polling(timeout=100, long_polling_timeout = 50)

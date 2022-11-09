from matplotlib.pyplot import switch_backend
from tok import *   
from random import randint 
import telebot 
from telebot import types
import random

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])  
def start(message):
    if message.text == "/start":
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)        #Создание разметки клавиатуры, кол-во кнопок в 1 строке
        btn1 = types.KeyboardButton(text = 'Играть')        #Создание кнопки
        btn2 = types.KeyboardButton(text = 'Позже') 
        kb.add(btn1, btn2)  # Добавляем кнопки в клавиатуру
        bot.send_message(message.chat.id, 
            f"Привет, {message.from_user.first_name}! Давай поиграем в Крестики-нолики )", reply_markup=kb)


 
# 1.Создание клавиатуры с callback кнопками (урок 13)
@bot.message_handler(content_types = ['text'])  
def game_start(message):
    if message.text == 'Позже':
        bot.send_message(message.chat.id, "Ну позже, так позже...")
    elif message.text == 'Играть':
        item = {}
        kb = types.InlineKeyboardMarkup(row_width=3)       #Создание разметки клавиатуры, кол-во кнопок в 1 строке
        for i in range(9):
            item[i] = types.InlineKeyboardButton(text = f'{i}', callback_data=str(i))
        kb.add(item[0], item[1], item[2])
        kb.add(item[3], item[4], item[5])
        kb.add(item[6], item[7], item[8])
    bot.send_message(message.chat.id, "Твой ход!", reply_markup=kb)
   

numbers = [0, 1, 2, 3, 4, 5, 6, 7, 8]
new_numbers = []
bot_numbers = []
@bot.callback_query_handler(func= lambda callback: callback.data)
def check_callback_data(callback):
    msg = callback.data
    items = msg.split() 
    x = int(items[0])
    if x in numbers:
        numbers.remove(x)
        new_numbers.append(x)
        new_numbers.sort()
        item = {}
        kb = types.InlineKeyboardMarkup(row_width=3)       
        for i in numbers:
            item[i] = types.InlineKeyboardButton(text = f'{i}', callback_data=str(i))
        for j in new_numbers:
            item[j] = types.InlineKeyboardButton(text = 'Х', callback_data=str(i))
        y = random.choice(numbers)
        numbers.remove(y)
        bot_numbers.append(y)
        for k in bot_numbers:
            item[k] = types.InlineKeyboardButton(text = 'O', callback_data=str(i))
        kb.add(item[0], item[1], item[2])
        kb.add(item[3], item[4], item[5])
        kb.add(item[6], item[7], item[8])
        win = ((0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6))
        if len(new_numbers) > 2:
            for all in win:
                count = 0
                for k in new_numbers:
                    if k in all:
                        count +=1
                if count == 3:    
                    bot.edit_message_text(chat_id = callback.message.chat.id, 
                    message_id=callback.message.id, text = 'Ты ПОБЕДИЛ!', reply_markup=kb)
           
        elif len(bot_numbers) > 2:
            for all in win:
                count = 0
                for k in bot_numbers:
                    if k in all:
                        count +=1
                if count == 3:    
                    bot.edit_message_text(chat_id = callback.message.chat.id, 
                    message_id=callback.message.id, text = 'Тебя выиграли...', reply_markup=kb) 

        else :
            bot.edit_message_text(chat_id = callback.message.chat.id, 
            message_id=callback.message.id, text = 'Ходи', reply_markup=kb) 

        
bot.polling()

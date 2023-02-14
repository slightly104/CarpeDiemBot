import telebot
from telebot import types
from config import TOKEN
import random


bot = telebot.TeleBot(TOKEN)

compliments = {
    "1": "Ты сверхмилая)",
    "2": "Ты самая красивая на свете! (Шепчу на ушко по утрам)",
    "3": "Тебе пойдет любая вещь которую ты выберешь)",
    "4": "У тебя уникальное и просто потрясающее чувство юмора!",
    "5": "Ты умна и загадочна, от того и притягательна",
    "6": "У тебя самый потрясающий муж, о котором можно только мечтать! Ты отлично умеешь выбирать)",
    "7": "Ты потрясающий музыкант, Семён тобой искренне восхищается!",
    "8": "Ты великолепно готовишь!",
    "9": "Ты рожаешь просто идеальных детей)))",
    "10": "ты любовь Семёна единственная и вечная… :*"
}


# Начало работы
@bot.message_handler(commands=["start"])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton('О самой прекрасной особе на планете')
    item2 = types.KeyboardButton('По-гадаем на книге которую ты выберешь')
    item3 = types.KeyboardButton('Секретный уровень')
    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id, 
    "Привет Нина, Семён меня создал чтобы развлечь тебя в его отсутствие.\nО чем поболтаем?", reply_markup=markup)


# Главное меню
def main_menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton('О самой прекрасной особе на планете')
    item2 = types.KeyboardButton('По-гадаем на книге которую ты выберешь')
    item3 = types.KeyboardButton('Секретный уровень')
    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id, "О чем поболтаем?", reply_markup=markup)


#Рубрика комплименты
def send_compliment(message):
    text = message.text
    if text == "Вернуться":
        main_menu(message)
    elif text not in compliments.keys():
        msg = bot.reply_to(message, "Семён тебя конечно любит, но давай по сценарию)")
        bot.register_next_step_handler(msg, send_compliment)  
    else:
        msg = bot.reply_to(message, compliments.get(text))
        bot.register_next_step_handler(msg, send_compliment)


# Рубрика гадание
def divination(message):
    text = message.text
    if text == "Вернуться":
        main_menu(message)
    elif text == "Гадай":
        page = random.randint(4, 300)
        line = random.randint(1, 20)
        bot.send_message(message.chat.id, f"Страница: {page}, строка: {line}!")
        msg = bot.send_message(message.chat.id, "Ещё?")
        bot.register_next_step_handler(msg, divination)
    else:
        msg = bot.send_message(message.chat.id, "Нажми 'Гадай' или 'Вернуться'")
        bot.register_next_step_handler(msg, divination)
        

# Секретный уровень
def secret(message):
    text = message.text
    
    if text == "Вернуться":
        main_menu(message)
    elif text == "12.05.2022":
        bot.send_message(message.chat.id, "В морозилке мороженка..)")
        main_menu(message)
    else:
        msg = bot.send_message(message.chat.id, "А это точно ты? Попробуй еще раз")
        bot.register_next_step_handler(msg, secret)  


# Текстовые запросы
@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':

        # О самой прекрасной особе на планете
        if message.text == 'О самой прекрасной особе на планете':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            item1 = types.KeyboardButton("Вернуться")
            markup.add(item1)
            msg = bot.send_message(message.chat.id,
            "Ты выбрала раздел «Комплименты»\nНабери цифру от 1 до 10", reply_markup=markup)
            bot.register_next_step_handler(msg, send_compliment)

        elif message.text == "По-гадаем на книге которую ты выберешь":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            item1 = types.KeyboardButton("Гадай")
            item2 = types.KeyboardButton("Вернуться")
            markup.add(item1, item2)
            msg = bot.send_message(message.chat.id,
            "Ты выбрала гадание", reply_markup=markup)
            bot.register_next_step_handler(msg, divination)

        elif message.text == "Секретный уровень":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
            item1 = types.KeyboardButton("Вернуться")
            markup.add(item1)
            msg = bot.send_message(message.chat.id,
            "Ты выбрала секретики", reply_markup=markup)
            bot.send_message(message.chat.id, "Введи дату вашей с Семёном свадьбы (чтобы убедиться что это точно ты):")
            bot.register_next_step_handler(msg, secret)

        else:
            bot.send_message(message.chat.id, "Семён тебя конечно любит, но давай по сценарию)")
            main_menu(message)


bot.infinity_polling()
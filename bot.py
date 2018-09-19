import logging
import datetime
from glob import glob
from random import choice

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, RegexHandler
from telegram import ReplyKeyboardMarkup, KeyboardButton

from emoji import emojize

import ephem

import settings


#Настройки лога
logging.basicConfig(format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level = logging.INFO,
	filename = 'bot.log'
	)


def astronom(bot, update,user_data):
	logging.info("User: %s, Chat id: %s, Message: %s",
	 update.message.chat.username,update.message.chat.id,
	  update.message.text)

	input_user = update.message.text
	input_user = input_user.split('planet')

	if len(input_user) != 2 :
		update.message.reply_text('после команды /planet, введите название одной планеты')
	else:
		input_user_this = input_user[1]
		input_user_this = input_user_this.strip()
		input_user_this = input_user_this.lower()

		date = datetime.datetime.now()
		date = date.strftime('%Y/%m/%d')

		text_planet = {}
		planet = {}

		if input_user_this == "меркурий":
			planet = ephem.Mercury(date)
			text_planet = ephem.constellation(planet)

		elif input_user_this == "венера":
			planet = ephem.Venus(date)
			text_planet = ephem.constellation(planet)

		elif input_user_this == "марс":
			planet = ephem.Mars(date)
			text_planet = ephem.constellation(planet)

		elif input_user_this == "юпитер":
			planet = ephem.Jupiter(date)
			text_planet = ephem.constellation(planet)

		elif input_user_this == "сатурн":
			planet = ephem.Saturn(date)
			text_planet = ephem.constellation(planet)

		elif input_user_this == "уран":
			planet = ephem.Uranus(date)
			text_planet = ephem.constellation(planet)

		elif input_user_this == "нептун":
			planet = ephem.Neptune(date)
			text_planet = ephem.constellation(planet)

		elif input_user_this == "плутон":
			planet = ephem.Pluto(date)
			text_planet = ephem.constellation(planet)
		
		signs = {"Aquarius": "Водолея", "Aries": "Овна", "Cancer": "Рака",
		 "Capricornus": "Козерога", "Gemini": "Близнецов", "Leo": "Льва",
		  "Libra": "Весов", "Ophiuchus": "Змееносца", "Pisces": "Рыб",
		   "Sagittarius": "Стрельца", "Scorpius": "Скорпиона",
		    "Taurus": "Тельца", "Virgo": "Девы"}

		for sign in signs:
			if text_planet[-1] == sign:
				update.message.reply_text("Сегодня {} проходит через созвездие {}".
					format(input_user[1],signs[text_planet[1]]))


def greet_user(bot,update,user_data):
	emo = get_user_emo(user_data)
	user_data['emo'] = emo
	text = 'Привет {}{}'.format(update.message.chat.first_name,emo)
	update.message.reply_text(text, reply_markup= get_keyboard())


def send_cat_picture(bot,update,user_data):
	cat_list = glob('images/notcat/*prog*.jpg')
	cat_pic = choice(cat_list)
	bot.send_photo(chat_id = update.message.chat_id, photo = open(cat_pic,'rb'), reply_markup= get_keyboard())


def change_avatar(bot,update,user_data):
	if 'emo' in user_data:
		del user_data['emo']
	emo = get_user_emo(user_data)
	update.message.reply_text('Готово {}'.format(emo), reply_markup= get_keyboard())


def word_count(bot,update,user_data):
	if update.message.text =='/wordcount':
		update.message.reply_text('''
			Вы не написали слов после команды.\nНе обижайте бота!
			''',reply_markup= get_keyboard())
	else:
		twosimbol = False
		count_text1 =""
		count_text = str(update.message.text)
	
		for simbol in count_text:
			if simbol == '"':
				twosimbol = not twosimbol

			if twosimbol ==  True:
					count_text1 += simbol
		count_text1 = count_text1.split(' ')
		num = len(count_text1)
		text ='{} {}'.format( num, rus_nuber(num))
		update.message.reply_text(text, reply_markup= get_keyboard())


def talk_to_me(bot, update, user_data):
	emo = get_user_emo(user_data)
	#принимаем текст от пользователя
	user_text = "Привет {}{}! Ты написал: {}".format(
		update.message.chat.first_name, emo, update.message.text)

	logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username, 
		update.message.chat.id, update.message.text)

	#отправляем текст пользователю
	update.message.reply_text(user_text, reply_markup= get_keyboard())


def get_contact(bot, update, user_data):
	print(update.message.contact)
	update.message.reply_text('Готово {}',format(get_user_emo(user_data)), reply_markup= get_keyboard())


def get_location(bot, update, user_data):
	print(update.message.location)
	update.message.reply_text('Готово {}',format(get_user_emo(user_data)), reply_markup= get_keyboard())


def get_keyboard():
	contact_button = KeyboardButton('Контактные данные', request_contact = True)
	locaton_button = KeyboardButton('Геолокация', request_location = True)

	contact_button = KeyboardButton('Даные', request_contact = True)
	locaton_button = KeyboardButton('Координаты', request_location = True)

	my_keyboard = ReplyKeyboardMarkup([
		['Прислать дем','Сменить аватарку'], 
		[contact_button,locaton_button]
		], resize_keyboard = True
		)
	return my_keyboard


def get_user_emo(user_data):
	if 'emo' in user_data:
		return user_data['emo']
	else:
		user_data['emo'] = emojize(choice(settings.USER_EMOJI), use_aliases = True)
		return user_data['emo']


def rus_nuber(num):
	if num >= 11 and num <= 19:
		word = 'слов'
	else:
		if num % 10 == 1:
			word = 'слово'
		elif num % 10 in (2,3,4):
			word = 'слова'
		else:
			word = 'слов'
	return word



def main():
	'''Тело бота. Главная функция.'''
	mybot = Updater(settings.API_KEY,
		request_kwargs=settings.PROXY)

	logging.info('бот запускается')
	
	dp = mybot.dispatcher
	dp.add_handler(CommandHandler("start", greet_user, pass_user_data=True))
	dp.add_handler(CommandHandler("planet", astronom, pass_user_data=True))
	dp.add_handler(CommandHandler('cat',send_cat_picture, pass_user_data=True))
	dp.add_handler(CommandHandler('wordcount',word_count, pass_user_data=True))
	
	dp.add_handler(RegexHandler('^(Прислать дем)$', send_cat_picture, pass_user_data = True))
	dp.add_handler(RegexHandler('^(Сменить аватарку)$', change_avatar, pass_user_data = True))
	
	dp.add_handler(MessageHandler(Filters.contact, get_contact, pass_user_data=True))
	dp.add_handler(MessageHandler(Filters.location, get_location, pass_user_data=True))
	dp.add_handler(MessageHandler(Filters.text, talk_to_me, pass_user_data=True))


	mybot.start_polling()
	mybot.idle()


main()
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import settings
import datetime
import ephem

#Настройки лога
logging.basicConfig(format= '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
	level = logging.INFO,
	filename = 'bot.log'
	)


def greet_user(bot,update):
	text = '😉'
	print(text)
	logging.info('text')
	update.message.reply_text(text)

def astronom(bot, update):

	logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username,update.message.chat.id, update.message.text)

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

		if input_user_this == "венера":
			planet = ephem.Venus(date)
			text_planet = ephem.constellation(planet)

		if input_user_this == "марс":
			planet = ephem.Mars(date)
			text_planet = ephem.constellation(planet)

		if input_user_this == "юпитер":
			planet = ephem.Jupiter(date)
			text_planet = ephem.constellation(planet)

		if input_user_this == "сатурн":
			planet = ephem.Saturn(date)
			text_planet = ephem.constellation(planet)

		if input_user_this == "уран":
			planet = ephem.Uranus(date)
			text_planet = ephem.constellation(planet)

		if input_user_this == "нептун":
			planet = ephem.Neptune(date)
			text_planet = ephem.constellation(planet)

		if input_user_this == "плутон":
			planet = ephem.Pluto(date)
			text_planet = ephem.constellation(planet)
		
		signs = {"Aquarius": "Водолея", "Aries": "Овна", "Cancer": "Рака", "Capricornus": "Козерога", "Gemini": "Близнецов", "Leo": "Льва", "Libra": "Весов", "Ophiuchus": "Змееносца", "Pisces": "Рыб", "Sagittarius": "Стрельца", "Scorpius": "Скорпиона", "Taurus": "Тельца", "Virgo": "Девы"}
		for sign in signs:
			if text_planet[-1] == sign:
				update.message.reply_text("Сегодня {} проходит через созвездие {}".format(input_user[1],signs[text_planet[1]]))
	

	user_log = "User: {}, Chat id: {}, Message: {}".format(update.message.chat.username,update.message.chat.id, update.message.text)
	update.message.reply_text(user_log)




def talk_to_me(bot, update):
	#принимаем текст от пользователя
	user_text = "Привет {}! Ты написал: {}".format(
		update.message.chat.first_name,update.message.text)

	logging.info("User: %s, Chat id: %s, Message: %s", update.message.chat.username, 
		update.message.chat.id, update.message.text)

	#отправляем текст пользователю
	update.message.reply_text(user_text)

def main():
	'''Тело бота. Главная функция.'''
	mybot = Updater(settings.API_KEY,
		request_kwargs=settings.PROXY)

	logging.info('бот запускается')
	
	dp = mybot.dispatcher
	dp.add_handler(CommandHandler("start", greet_user))
	dp.add_handler(CommandHandler("planet", astronom))
	dp.add_handler(MessageHandler(Filters.text, talk_to_me))


	mybot.start_polling()
	mybot.idle()


main()
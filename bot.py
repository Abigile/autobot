from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import settings

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
	dp.add_handler(MessageHandler(Filters.text, talk_to_me))


	mybot.start_polling()
	mybot.idle()


main()
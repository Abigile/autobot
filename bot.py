from telegram.ext import Updater, CommandHandler

PROXY = {'proxy_url':'socks5://t1.learn.python.ru:1080',
'urllib3_proxy_kwargs':{'username':'learn','password':'python'}}

def main():
	'''Тело бота. Главная функция.'''
	mybot = Updater("659874606:AAH7vMN9q6Lxrcj2J0LRSRX9tfn3L", 
		request_kwargs=PROXY)

	dp = mybot.dispatcher
	dp.add_handler(CommandHandler("start", greet_user))

	mybot.start_polling()
	mybot.idle()

main()
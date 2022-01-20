import requests
import telebot
from bs4 import BeautifulSoup
from pyowm import OWM
from pyowm.utils.config import get_default_config

bot = telebot.TeleBot("5198083670:AAH8Td_aoWI9a1BIQcAxMDFmtC_BuzqwJoU")

@bot.message_handler(commands=['start'])
def start(message):
	bot.send_message(message.chat.id, 'Добро пожаловать, ' + str(message.from_user.first_name) +
					 ',\nЧтобы узнать погоду напишите в чат название города' +
					 ',\nЧтобы узнать последние новости напишите в чат "/Новости"' +
					 ',\nЕсли забыли команды напишите в чат "/Помощь"')

@bot.message_handler(commands=['Новости'])
def start(message):
	text = message.text
	if text == "новости" or "Новости":
		page = requests.get("https://ria.ru/world/")
		x = page.content
		soup = BeautifulSoup(x, 'html.parser')
		html = soup.findAll('a', class_="list-item__title color-font-hover-only")
		news = []
		for data in html:
			news.append(data.get('href'))
			if len(news) == 3:
				break
		for i in news:
			bot.send_message(message.chat.id, text=i)

@bot.message_handler(commands=['Помощь'])
def start(message):
	bot.send_message(message.chat.id, 'Добро пожаловать, ' + str(message.from_user.first_name) +
					 ',\nЧтобы узнать погоду напишите в чат название города' +
					 ',\nЧтобы узнать последние новости напишите в чат "/Новости"')

@bot.message_handler(content_types=['text'])
def test(message):
	try:
		place = message.text
		config_dict = get_default_config()
		config_dict['language'] = 'ru'
		owm = OWM('bb78a35feaa4f01ddd88f0b0e68f6574', config_dict)
		mgr = owm.weather_manager()
		observation = mgr.weather_at_place(place)
		w = observation.weather
		t = w.temperature("celsius")
		t1 = t['temp']
		t2 = t['feels_like']
		t3 = t['temp_max']
		t4 = t['temp_min']
		wi = w.wind()['speed']
		humi = w.humidity
		pr = w.pressure['press']
		bot.send_message(message.chat.id, "В городе " + str(place) + " температура " + str(t1) + " °C" + "\n" +
				"Максимальная температура " + str(t3) + " °C" +"\n" +
				"Минимальная температура " + str(t4) + " °C" + "\n" +
				"Ощущается как" + str(t2) + " °C" + "\n" +
				"Скорость ветра " + str(wi) + " м/с" + "\n" +
				"Давление " + str(pr) + " мм.рт.ст" + "\n" +
				"Влажность " + str(humi) + " %" + "\n")
	except:
		bot.send_message(message.chat.id, "Такой город не найден!")
		print(str(message.text), "- не найден")
		print('hi')

bot.polling(none_stop=True, interval=0)

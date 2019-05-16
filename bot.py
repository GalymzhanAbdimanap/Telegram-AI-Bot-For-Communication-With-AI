from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import apiai, json
from flask import Flask


server = Flask(__name__)


updater = Updater(token='895277021:AAEF6pBhDJwe4-pajLq_dym0CrlY8HlCfvU') # Токен API к Telegram
dispatcher = updater.dispatcher
# Обработка команд
@server.route("/")
def startCommand(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text='Привет, давай пообщаемся?')
    return "data"
def textMessage(bot, update):
    request = apiai.ApiAI('7e7dba808f2a40779eb16763af566ce4').text_request() # Токен API к Dialogflow
    request.lang = 'ru' # На каком языке будет послан запрос
    request.session_id = 'SatpayevsBot' # ID Сессии диалога (нужно, чтобы потом учить бота)
    request.query = update.message.text # Посылаем запрос к ИИ с сообщением от юзера
    responseJson = json.loads(request.getresponse().read().decode('utf-8'))
    response = responseJson['result']['fulfillment']['speech'] # Разбираем JSON и вытаскиваем ответ
    # Если есть ответ от бота - присылаем юзеру, если нет - бот его не понял
    if response:
        bot.send_message(chat_id=update.message.chat_id, text=response)
    else:
        bot.send_message(chat_id=update.message.chat_id, text='Я Вас не совсем понял!')
# Хендлеры
start_command_handler = CommandHandler('start', startCommand)
text_message_handler = MessageHandler(Filters.text, textMessage)
# Добавляем хендлеры в диспетчер
dispatcher.add_handler(start_command_handler)
dispatcher.add_handler(text_message_handler)
# Начинаем поиск обновлений
updater.start_polling(clean=True)
# Останавливаем бота, если были нажаты Ctrl + C
updater.idle()

if __name__="__main__":
    server.run(host="0.0.0.0", port=5000)

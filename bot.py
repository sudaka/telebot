import telebot
from telebot import types
from botdjangoint import Config
from botdjangoint import ChatUserInterface

curconfig = Config()
chatui = ChatUserInterface()
gamebot = telebot.TeleBot(token=curconfig.token)

def sendactivatemessage(curchatid):
    mkp = chatui.createpackmarkup()
    gamebot.send_message(curchatid, curconfig.activatemessage, reply_markup=mkp)

@gamebot.message_handler(commands=['start'])
def start(message):
    curchatid = message.chat.id
    if chatui.checkchatid(curchatid):
        if chatui.isactivateduser(curchatid):
            pass
        else:
            gamebot.send_message(curchatid, curconfig.hellonotactivateduser)
    else:
        curname = message.from_user.last_name
        if chatui.addnewuser(curchatid, curname):
            gamebot.send_message(curchatid, curconfig.hellonewuser)
            gamebot.send_message(curconfig.superuserchatid, f'Добавлен новый клиент. Имя:{curname} ИД:{curchatid}')
        else:
            gamebot.send_message(curconfig.superuserchatid, f'При добавлении нового клиента (имя:{curname} ИД:{curchatid}) произошла ошибка.')
        
@gamebot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'Назад':
        mkp = chatui.createpackmarkup()
        chatui.gotopacklist(call.from_user.id)
        gamebot.send_message(call.from_user.id, curconfig.packmessage, reply_markup=mkp)
    elif str(call.data).isdigit():
        cardtxt = chatui.getcarddata(call.from_user.id, call.data)
        if chatui.iscardjpg(call.from_user.id):
            gamebot.send_photo(call.from_user.id, str(cardtxt))
        else:
            gamebot.send_message(call.from_user.id, cardtxt)
        mkp = chatui.createpackmarkup()
        chatui.gotopacklist(call.from_user.id)
        gamebot.send_message(call.from_user.id, curconfig.packmessage, reply_markup=mkp)
    else:
        mrkp = chatui.createcardmarkup(call.from_user.id, call.data)
        gamebot.send_message(call.from_user.id, 'Выберите карту', reply_markup=mrkp)
    #print(call.from_user.id)
    #call.data    

if __name__ == '__main__':
    gamebot.infinity_polling()

import telebot
from telebot import types
from botdjangoint import Config
from botdjangoint import ChatUserInterface
import re
from imgcreator import Multiline
from cupidongame import settings as cursettings
import os

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
            mrk = chatui.createreplyadmingetaccessmarkup(curchatid)
            #mrk = telebot.types.ReplyKeyboardRemove()
            gamebot.send_message(
                curconfig.superuserchatid, 
                f'Добавлен новый клиент, нужно его активировать. Имя:{curname} ИД:{curchatid}', 
                reply_markup=mrk)
        else:
            gamebot.send_message(curconfig.superuserchatid, f'При добавлении нового клиента (имя:{curname} ИД:{curchatid}) произошла ошибка.')

'''
@gamebot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    try:
        gamebot.delete_message(call.from_user.id, call.message.message_id)
    except:
        print('Imessageid:', call.message.message_id, 'Chatid:', call.from_user.id)
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
    elif re.search(r'^#\d+-\d+$', call.data):
        cstep = chatui.getcurstep(call.from_user.id)
        mrkp = chatui.createcardmarkup(call.from_user.id, cstep, call.data)
        gamebot.send_message(call.from_user.id, 'Выберите карту или перейдите на следующую страницу', reply_markup=mrkp)
    else:
        mrkp = chatui.createcardmarkup(call.from_user.id, call.data)
        gamebot.send_message(call.from_user.id, 'Выберите карту', reply_markup=mrkp)
    #print(call.from_user.id)
    #call.data 
'''   


@gamebot.message_handler(func=lambda message:True)
def all_messages(message):
    df = re.match(r'^(id:(\d+):Активировать)$', message.text)
    if message.text == 'Назад':
        mkp = chatui.createreplypackmarkup()
        chatui.gotopacklist(message.chat.id)
        gamebot.send_message(message.chat.id, curconfig.packmessage, reply_markup=mkp)
    elif str(message.text).isdigit():
        cardtxt = chatui.getcarddata(message.chat.id, message.text)
        if chatui.iscardjpg(message.chat.id):
            gamebot.send_photo(message.chat.id, str(cardtxt))
        elif chatui.iscardcreatingjpg(message.chat.id):
            imgdir = cursettings.PAGEN_BACKGROUND_ROOT
            background = cursettings.PAGEN_BACKGROUND_FILE
            textpercent = cursettings.PAGEN_SQUAREFORTEXT
            font = cursettings.PAGEN_FONTFILE
            txtimg = Multiline(str(cardtxt))
            httpurl = cursettings.PAGEN_URL
            curfname = txtimg.createfilename(background, font, textpercent)
            if len(curfname) > 1:
                fullpath = os.path.join(imgdir, f'{curfname}_{background}')
                if txtimg.checkfilebyname(fullpath):
                    gamebot.send_photo(message.chat.id, str(f'{httpurl}{curfname}_{background}'))
                else:
                    gamebot.send_message(message.chat.id, 'Ошибка получения файла изображения')
        else:
            gamebot.send_message(message.chat.id, cardtxt)
        mkp = chatui.createreplypackmarkup()
        chatui.gotopacklist(message.chat.id)
        gamebot.send_message(message.chat.id, curconfig.packmessage, reply_markup=mkp)
    elif df:
        if str(message.chat.id) == curconfig.superuserchatid:
            chid = df.group(2)
            if chatui.activateuser(chid):
                sendactivatemessage(chid)
                mkp = chatui.createreplypackmarkup()
                chatui.gotopacklist(message.chat.id)
                gamebot.send_message(message.chat.id, curconfig.packmessage, reply_markup=mkp)
    else:
        mrkp = chatui.createreplymarkup(message.chat.id, message.text)
        gamebot.send_message(message.chat.id, 'Выберите карту', reply_markup=mrkp)

if __name__ == '__main__':
    gamebot.infinity_polling()

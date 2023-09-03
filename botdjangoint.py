import os
import django
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

script_path = os.path.dirname(__file__)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cupidongame.settings')
django.setup()

from botbackend import models

class Config():
    def __init__(self):
        self.token = '6682619083:AAFYodFdpjMoh6fsRxg6JNXUbSNrLk9NhkI'
        self.superuserchatid = '435177751'
        self.packinrow = 1
        self.cardsinrow = 8
        self.hellonewuser = '''
        Добро пожаловать! Запрос на предоставление доступа направлен. Ожидайте подтверждение доступа.
        '''
        self.hellonotactivateduser = 'Запрос на активацию Вашей учетной записи направлен. Пожалуйста, ожидайте сообщения с подтверждением.'
        self.activatemessage = 'Ваш доступ к чату активирован!'
        self.packmessage = 'Выберите колоду'


class ChatUserInterface():
    def __init__(self) -> None:
        self.model = models.Chatusers

    def checkchatid(self, tmpchatid):
        idinbd = False
        idlist = models.Chatusers.objects.filter(chatid=tmpchatid)
        if len(idlist) > 0:
            idinbd = True
        return idinbd
    
    def isactivateduser(self, tmpchatid):
        isactivated = False
        idlist = models.Chatusers.objects.filter(chatid=tmpchatid) & models.Chatusers.objects.filter(isactive=True)
        if len(idlist) == 1:
            isactivated = True
        return isactivated
    
    def addnewuser(self, newchatid, newname):
        nu = models.Chatusers.objects.create(chatid=newchatid, name=newname, isactive=False)
        if nu.id > 0:
            return True
        else:
            return False

    def createpackmarkup(self):
        curset = Config()
        markup = InlineKeyboardMarkup()
        markup.row_width = curset.packinrow
        packs = models.Pack.objects.all()
        for pack in packs:
            markup.add(InlineKeyboardButton(pack.name, callback_data=str(pack.name)))
        return markup
    
    def createcardmarkup(self, chatid, packname):
        curset = Config()
        markup = InlineKeyboardMarkup()
        markup.row_width = curset.cardsinrow
        try:
            packobj = models.Pack.objects.get(name=packname)
        except models.Pack.DoesNotExist:
            packobj = None
        if packobj:
            try:
                chatusr = models.Chatusers.objects.get(chatid=chatid)
            except models.Chatusers.DoesNotExist:
                chatusr = None
            if chatusr:
                chatusr.curstep = packobj
                chatusr.save()
                cards = models.Card.objects.filter(pack = packobj)
                currow = []
                for card in cards:
                    currow.append(InlineKeyboardButton(card.number, callback_data=str(card.number)))
                    if len(currow) >= curset.cardsinrow:
                        markup.row(*currow)
                        currow = []
                if len(currow) > 0:
                    markup.row(*currow)
                markup.row(InlineKeyboardButton('Назад', callback_data='Назад'))
        return markup
    
    def gotopacklist(self, chatid):
        try:
            chatusr = models.Chatusers.objects.get(chatid=chatid)
        except models.Chatusers.DoesNotExist:
            chatusr = None
        if chatusr:
            chatusr.curstep = None
            chatusr.save()

    def getcarddata(self, chatid, cardnumber):
        curtext = ''
        try:
            chatusr = models.Chatusers.objects.get(chatid=chatid)
        except models.Chatusers.DoesNotExist:
            chatusr = None
        if chatusr:
            curpack = chatusr.curstep
            try:
                curcard = models.Card.objects.get(pack=curpack, number=cardnumber)
                curtext = curcard.cardtext
            except:
                curtext = 'Карточка не найдена'
        return curtext
    
    def iscardjpg(self, chatid):
        try:
            chatusr = models.Chatusers.objects.get(chatid=chatid)
        except models.Chatusers.DoesNotExist:
            chatusr = None
        if chatusr:
            curpack = chatusr.curstep
            if curpack.packtype == 'IMG':
                return True
        return False

import os
import django
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

script_path = os.path.dirname(__file__)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cupidongame.settings')
django.setup()

from botbackend import models

class Config():
    def __init__(self):
        self.token = '6682619083:AAFYodFdpjMoh6fsRxg6JNXUbSNrLk9NhkI'
        self.superuserchatid = '435177751'
        self.paginatecount = 50
        self.packinrow = 1
        self.cardsinrow = 5
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
    
    def createcardmarkup(self, chatid, packname, curpag = ''):
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
                if len(cards) < curset.paginatecount:
                    for card in cards:
                        currow.append(InlineKeyboardButton(card.number, callback_data=str(card.number)))
                        if len(currow) >= curset.cardsinrow:
                            markup.row(*currow)
                            currow = []
                    if len(currow) > 0:
                        markup.row(*currow)
                else:
                    pcards = self.getpaginated(cards)
                    if curpag not in pcards.keys():
                        pagpcardsone = list(pcards.keys())
                        pagpcards = pcards[pagpcardsone[0]]
                    else:
                        pagpcards = pcards[curpag]
                    for card in pagpcards:
                        currow.append(InlineKeyboardButton(card.number, callback_data=str(card.number)))
                        if len(currow) >= curset.cardsinrow:
                            markup.row(*currow)
                            currow = []
                    if len(currow) > 0:
                        markup.row(*currow)
                    for pnames in pcards.keys():
                        markup.row(InlineKeyboardButton(pnames, callback_data=pnames))
                markup.row(InlineKeyboardButton('Назад', callback_data='Назад'))
        return markup
    
    def createreplyadmingetaccessmarkup(self, chat_id):
        curset = Config()
        markup = ReplyKeyboardMarkup()
        markup.add(KeyboardButton(f'id:{chat_id}:Активировать'))
        markup.add(KeyboardButton('Назад'))
        return markup
    
    def activateuser(self, chat_id):
        res = True
        try:
            activateduser = models.Chatusers.objects.filter(chatid = chat_id)
            if activateduser:
                activateduser[0].isactive = True
                activateduser[0].save()
        except Exception as e:
            res = False
        return res
            
    def createreplypackmarkup(self):
        curset = Config()
        markup = ReplyKeyboardMarkup(row_width=curset.packinrow)
        packs = models.Pack.objects.all()
        for pack in packs:
            markup.add(KeyboardButton(pack.name))
        return markup

    def createreplymarkup(self, chatid, packname):
        curset = Config()
        markup = ReplyKeyboardMarkup(row_width=curset.cardsinrow)
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
                    currow.append(KeyboardButton(card.number))
                    if len(currow) >= curset.cardsinrow:
                        markup.add(*currow)
                        currow = []
                if len(currow) > 0:
                    markup.add(*currow)
                markup.row(KeyboardButton('Назад'))
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
    
    def getpaginated(self, lst):
        curset = Config()
        countpaginate = curset.paginatecount
        lcount = len(lst)
        abscount = lcount // countpaginate
        newpaglist = {}
        for m in range(abscount):
            paglist = lst[m*countpaginate:(m+1)*countpaginate]
            tmpkey = f'#{m*countpaginate}-{(m+1)*countpaginate}'
            newpaglist[tmpkey] = paglist
        lastpag = []
        lastpag = lst[abscount*countpaginate:]
        tmpkey = f'#{abscount*countpaginate}-{lcount}'
        newpaglist[tmpkey] = lastpag
        return newpaglist
    
    def getcurstep(self, chatid):
        cstep = None
        try:
            chatusr = models.Chatusers.objects.get(chatid=chatid)
        except models.Chatusers.DoesNotExist:
            chatusr = None
        if chatusr:
            cstep = chatusr.curstep.name
        return cstep

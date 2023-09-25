import PIL
from PIL import Image, ImageFont, ImageDraw
import textwrap
import hashlib
import os

class Multiline():
    def __init__(self, line = ''):
        self.line = line
    
    def getmaxsplit(self):
        mlist = self.line.split()
        return len(mlist)
    
    def getminchars(self):
        mlist = self.line.split()
        minchars = 0
        for sl in mlist:
            if len(sl) > minchars:
                minchars = len(sl)
        return minchars
    
    def findmaxsquare(self, fname, squarepercentfortext = 0.8, fontpath = ''):
        image = Image.open(fname)
        (w, h) = image.size # w - ширина h - высота
        image.close()
        sqrsquare = squarepercentfortext ** 0.5
        wmax = w * sqrsquare
        hmax = h * sqrsquare
        maxtextsquare = hmax * wmax
        charcountout = 0
        fontsizecount = 0
        maxsquare = 0
        lastlist = ''
        for charcount in range(self.getminchars(), len(self.line)+1):
            curfontsize = 10
            dtext = textwrap.fill(self.line, charcount)
            if lastlist == dtext:
                continue
            else:
                lastlist = dtext
                while True:
                    image = Image.open(fname)
                    font = ImageFont.truetype(fontpath, curfontsize)
                    pencil = ImageDraw.Draw(image)
                    (left, top, right, bottom) = pencil.multiline_textbbox((0,0), dtext, font=font)
                    tmpw = right - left
                    tmph = bottom - top
                    if tmpw * tmph > maxtextsquare:
                        break
                    if tmpw * tmph > maxsquare and tmpw < wmax and tmph < hmax:
                        maxsquare = tmpw * tmph
                        fontsizecount = curfontsize
                        charcountout = charcount
                    curfontsize += 1
        return (fontsizecount, charcountout)
    
    def createfilename(self, backimagefname = '', fontfname = '', fpercent = 1):
        hashname = f'{backimagefname}{fontfname}{fpercent}{self.line}'.encode('utf-8')
        nhashname = int(hashlib.md5(hashname).hexdigest(), 16)
        outname = f'{nhashname}'
        return outname[:10]
    
    def createjpgmessage(self, fname, fontpath, fpercent, basedir):
        fnamefull = os.path.join(basedir, f'{fname}')
        fontpathfull = os.path.join(basedir, f'{fontpath}')
        genfname = self.createfilename(fname, fontpath, fpercent)
        (fontsizecount, charcountout) = self.findmaxsquare(fnamefull, squarepercentfortext=fpercent, fontpath=fontpathfull)
        dtext = textwrap.fill(self.line, charcountout)
        try:
            image = Image.open(fnamefull)
            (w, h) = image.size
            font = ImageFont.truetype(fontpathfull, fontsizecount)
            pencil = ImageDraw.Draw(image)
            w1 = w // 2
            h1 = h // 2
            pencil.multiline_text((w1, h1), dtext, font=font, fill='black', anchor="mm", align='center')
            fullpath = os.path.join(basedir, f'{genfname}_{fname}')
            image.save(fullpath)
        except:
            fullpath = ''
        return fullpath
    
    def checkfilebyname(self, fullfname = ''):
        if os.path.isfile(fullfname):
            return True
        else:
            return False
#BU KÜTÜPHANELER MOUSE NESNESI İÇİN
from ctypes import windll, Structure, c_long, byref
import win32gui, win32api, win32con

#SLEEP(saniye) BEKLEME FONKSİYONU
from time import sleep

#PYAUTOGUI BILGISAYAR EKRAN ÇÖZÜNÜRLÜĞÜNÜ ÖĞRENMEK İÇİN
import pyautogui as pag

#SERI PORT VE SYSTEM KÜTÜPHANELERI
import sys
import glob
import serial

#AKTIF SERI PORTLARI LISTELEMEK IÇIN KULLANILAN FONKSIYON
def seriPortListele():
    #WINDOWS ÜSTÜNDE ÇALIŞIYORSA
    if sys.platform.startswith('win'):
        portlar = ['COM%s' % (i + 1) for i in range(256)]
    
    #LINUX VEYA CYGWIN ÜSTÜNDE ÇALIŞIYORSA
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        portlar = glob.glob('/dev/tty[A-Za-z]*')
    else:
        raise EnvironmentError('Desteklenmeyen Platform!!!')

    sonuc = []
    #PORTLARI TEST ET, ÇALIŞANLARI SONUC DIZISINE AT
    for port in portlar:
        try:
            s = serial.Serial(port)
            s.close()
            sonuc.append(port)
        except (OSError, serial.SerialException):
            pass
    return sonuc


print("# SERI PORTLAR")
portlar = seriPortListele()

#PORT SEÇERKEN OLUŞACAK HATALARA KARŞI SONSUZ DÖNGÜ
while True:
    #SERI PORT LISTELEME
    for port in portlar:
        print("\t># "+str(port))

    #SERI PORT ADI
    secPort = input("\n>> SERI PORT ADI : ")

    #SERI PORT HABERLEŞME HIZI (ARDUINODA GENELDE 9600 KULLANILIR)
    secBaud = int(input("\n>> HABERLEŞME HIZI (BaudRate) : "))

    #SEÇILAN PORT AKTIF MI?
    if(secPort in portlar):
        #AKTIFSE DÖNGÜDEN ÇIK
        break
    else:
        #AKTIF DEĞİLSE BAŞA DÖN
        print("# BÖYLE BIR SERI PORT YOK!")

#SEÇILEN PORT VE BAUDRATE ILE ARDUİNOYA BAĞLAN
arduino = serial.Serial(secPort, secBaud)

#HASSASIYET SEÇİMİ HATALARINA KARŞI SONSUZ DÖNGÜ
while True:
    hassasiyet = 1;


    hass = [10,9,8,7,6,5,4,3,2,1]
    hassasiyetSec = int(input("\n>> HASSASIYET [1-10] : "))
    #HASSASIYET 1 İLE 10 ARASINDA DEĞİL Mİ ?
    if(hassasiyetSec < 1 or hassasiyet > 10):
        #BAŞA DÖN BİR DAHA SEÇ
        print("# GEÇERLI BIR DEĞER GIRMEDIN")
    else:
        #DIZIDEN HASSASIYETI ÇEK
        hassasiyet = int(hass[hassasiyetSec-1])
        #DÖNGÜDEN ÇIK
        break


#MOUSE NESNESI
#CTYPE KÜTÜPHANESİNE
#HAKİM OLMADIĞIM İÇİN
#HAZIR KOD PARÇASI KULLANDIM
class Mouse:
    MOUSEEVENTF_MOVE = 0x0001 # mouse move 
    MOUSEEVENTF_LEFTDOWN = 0x0002 # left button down 
    MOUSEEVENTF_LEFTUP = 0x0004 # left button up 
    MOUSEEVENTF_RIGHTDOWN = 0x0008 # right button down 
    MOUSEEVENTF_RIGHTUP = 0x0010 # right button up 
    MOUSEEVENTF_MIDDLEDOWN = 0x0020 # middle button down 
    MOUSEEVENTF_MIDDLEUP = 0x0040 # middle button up 
    MOUSEEVENTF_WHEEL = 0x0800 # wheel button rolled 
    MOUSEEVENTF_ABSOLUTE = 0x8000 # absolute move 
    SM_CXSCREEN = 0
    SM_CYSCREEN = 1

    def _get_button_value(self, button_name, button_up=False):
        buttons = 0
        if button_name.find("sag") >= 0:
            buttons = self.MOUSEEVENTF_RIGHTDOWN
        if button_name.find("sol") >= 0:
            buttons = buttons + self.MOUSEEVENTF_LEFTDOWN
        if button_name.find("orta") >= 0:
            buttons = buttons + self.MOUSEEVENTF_MIDDLEDOWN
        if button_up:
            buttons = buttons << 1
        return buttons

    def Tikla(self, button_name= "sol"):
        windll.user32.mouse_event(self._get_button_value(button_name, False)+self._get_button_value(button_name, True), 0, 0, 0, 0)

class POINT(Structure):
    _fields_ = [("x", c_long), ("y", c_long)]

#MOUSE GEÇERLİ POZİSYONU ÇEKME
def mousePos():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return { "x": pt.x, "y": pt.y}

#X, Y DEĞERLERINE GÖRE MOUSE POZISYONU AYARLAMA
def mouseGit(X,Y):
    windll.user32.SetCursorPos(X, Y)

#EKRAN ÇÖZÜNÜRLÜĞÜ
ekran = pag.size()
ekranX = ekran[0]
ekranY = ekran[1]

#MOUSE GEÇERLİ POZİSYONU
pos = mousePos()
posX  = int(pos['x'])
posY  = int(pos['y'])

#MOUSE NESNESI
mouse = Mouse()

print("\n# 3 SANIYE ICINDE BASLIYOR...")
print("\n# DURDURMAK ICIN \">> 'CTRL+C' <<\"")
sleep(3)

#SONSUZ DÖNGÜYE GİR
while True:
    #ARDUİNO SERİ PORT SON SATIR DEĞERİNİ OKU
    deger     = arduino.readline()

    #BYTE OLARAK GELEN DEĞERİ STRİNGE DÖNÜŞTÜR
    yeniDeger = deger.decode('utf-8')
    #SON 2 KARAKTER OLAN '\n\r' KARAKTERLERINI SİL
    yeniDeger = yeniDeger[:-2]

    # ',' KARAKTERLERI OLAN KISIMDAN BÖL VE koordinat DIZISINE ATA
    koordinat = yeniDeger.split(',')

    #GELEN X KOORDINATI
    koorX     = int(koordinat[0])
    #HASSASIYET AYARI
    koorX     = int(koorX/hassasiyet)

    #GELEN Y KOORDINATI
    koorY     = int(koordinat[1])
    #HASSASIYET AYARI
    koorY     = int(koorY/hassasiyet)

    #GELEN SOL BUTON BASMA DEĞERI (1 veya 0)
    koorSol   = int(koordinat[2])
    #GELEN SOL BUTON BASMA DEĞERI (1 veya 0)
    koorSag   = int(koordinat[3])

    #EĞER MOUSE_X POZISYONU, EKRAN BAŞINDAYSA
    if(posX>=ekranX)
        #MOUSE POZISYONU = EKRAN SINIRI
        posX=ekranX
    #EĞER MOUSE_X POZISYONU, EKRAN BAŞINDAYSA
    elif(posX<=0):
        #MOUSE POZISYONU = 0
        posX=0
    
    #EĞER MOUSE_Y POZISYONU, EKRAN BAŞINDAYSA
    if(posY>=ekranY)
        #MOUSE POZISYONU = EKRAN SINIRI
        posY=ekranY
    #EĞER MOUSE_Y POZISYONU, EKRAN BAŞINDAYSA
    elif(posY<=0):
        #MOUSE POZISYONU = 0
        posY=0
    
    #GELEN DEĞERLER -10 ile 10 ARASINDA DEĞİLSE
    if(koorX<(-10/hassasiyet) or koorX>(10/hassasiyet)):
        #MOUSE_X, KOORDINAT_X KADAR ARTTIR
        posX += koorX

    #GELEN DEĞERLER -10 ile 10 ARASINDA DEĞİLSE
    if(koorY<(-10/hassasiyet) or koorY>(10/hassasiyet)):
        #MOUSE_Y, KOORDINAT_Y KADAR ARTTIR
        posY += koorY
    
    #SOL BUTONA TIKLANDIYSA
    if(koorSol==0):
        #SOL TIKLA
        mouse.Tikla("sol")
        sleep(0.05)

    #SAG BUTONA TIKLANDIYSA
    if(koorSag==0):
        #SAG TIKLA
        mouse.Tikla("sag")
        sleep(0.05)
    
    #MOUSE'U HAREKET ETTIR
    mouseGit(posX, posY)
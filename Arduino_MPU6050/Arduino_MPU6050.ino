/*
 * MPU6050 GYRO_MOUSE
 * ATAKAN ARGIN
 * github : github.com/atakanargn
 */
 
//MPU6050 I2C PROTOKOLÜ ILE HABERLEŞİR
#include   <I2Cdev.h>
//MPU6050 Kütüphanesi
#include   <MPU6050.h>
#include   <Wire.h>

 /*
   MPU6050     ARDIUNO
    GND------- > GND
    VCC--------> +3V3
    SDA--------> A4
    SCL-------- > A5
    INT--------  >PIN 2

   SOL TIK BUTONU --> PIN9
   SAĞ TIK BUTONU --> PIN8
*/

//MPU6050 Tanımlama
MPU6050 GYRO;

int16_t accx, accy, accz; //IVME
int16_t gyrx, gyry, gyrz; //GYRO

int Xdeger, Ydeger;
int btnSol;
int btnSag;

char veri[30];

void setup()
{
    Serial.begin(9600);
    GYRO.initialize();
    //PULLUP direnç bağlamamak için INPUT_PULLUP
    pinMode(8,INPUT_PULLUP);
    pinMode(9, INPUT_PULLUP);

    //2 SANIYE BEKLE
    delay(2000);
}

void loop()
{
    //6 EKSENI DE AL TANIMLANAN DEĞİŞKENLERE ATA
    GYRO.getMotion6(&accx, &accy, &accz, &gyrx, &gyry ,&gyrz);
    
    btnSol=digitalRead(8); //SOL BUTON DEĞER OKUMA
    btnSag=digitalRead(9); //SAĞ BUTON DEĞER OKUMA

    //IVMEDEN YARARLANICAZ
    //Sensör normalde -17000 ile 17000 arası
    //değer verir, bu da ilk defa kullananların
    //MPU6050de bozukluk olduğunu düşünmesine sebep olabilir.

    //-17000 ile 17000 arası değeri 180 ile -180 arasına uyarladık
    //Siz bu değeri 0 ile 180 yapabilirsiniz
    //ancak değerin negatifliğinden yararlanıcaz
    Xdeger=map(accx,-17000,17000,180,-180);
    Ydeger=map(accy,-17000,17000,-180,180);

    //Değerleri veri fonksiyonuna atamak için kullanılan fonksiyon sprintf()
    sprintf(veri, "%d,%d,%d,%d", Xdeger, Ydeger, btnSol, btnSag);

    //Son olarak elimizdekileri Serial e yazdırdık
    Serial.println(veri);
    
    delay(20);
 }

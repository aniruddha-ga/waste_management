

#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
#include <UniversalTelegramBot.h> // THIS LIBRARY TO BE DOWNLOAD FROM LIBRARY MANAGER

const char* ssid = "Wifi Name";// Enter your WIFI SSID
const char* password = "Pass1234"; // Enter your WIFI Password

char link1[50] = "http://maps.google.com/maps?q=loc:";
char link2[50];
char link[100];

int var;
int trig = 13;
int echo = 12;
int buz=5;
int led =16;
long distance;
int duration;

#define BOTtoken "" // Enter the bottoken you got from botfather
#define CHAT_ID "" // Enter your chatID you got from chatid bot


X509List cert(TELEGRAM_CERTIFICATE_ROOT);
WiFiClientSecure client;
UniversalTelegramBot bot(BOTtoken, client);


void setup() 
{
  Serial.begin(9600);
   pinMode(trig,OUTPUT);
   pinMode(echo,INPUT);
   pinMode( buz,OUTPUT);
   pinMode(led,OUTPUT);
}

void gps()
{ 
  int i=0;
  float lat,lon;
  char inByte;
  char latitude[20],longitude[20],lati[20];
  float latmin,lonmin;
  int latdeg,londeg;
//==================== searching for "GG" ===================//
    do
    {
        do
        {
            while ( !Serial.available() );    
        } while ( 'G' != Serial.read() );                    // reading a character from the GPS
      
        while(!Serial.available());
    } while ( 'G' != Serial.read() );
//==================== searching for "GG" ===================//
 
//============== seeking for north cordinate ==============//
    do
    {
        while ( !Serial.available() );                       // reading a character from the GPS    
    } while ( ',' != Serial.read() );
 
    do
    {
        while ( !Serial.available() );                       // reading a character from the GPS
    } while ( ',' != Serial.read() );
//============== seeking for north cordinate ==============//
 
//============== printing the north cordinate ===============//
    //Serial.print(" N: ");
    do
    {
        while ( !Serial.available() ); 
        inByte = Serial.read();
        latitude[i]=inByte;
        i++;
        //Serial.write(latitude);     // reading a character from the GPS
        //Serial.write ( inByte );                             // printing the Latitude
    } while ( ',' != inByte );
        i--;
        latitude[i]='\0';
    //Serial.write(latitude);
    i=0;
//============== printing the north cordinate ===============//
 
//============== seeking for east cordinate ==============//
    do
    {
        while ( !Serial.available() );                       // reading a character from the GPS
    } while ( ',' != Serial.read() );
//============== seeking for east cordinate ==============//
 
//============== printing the east cordinate ===============//
    //Serial.print(" E: ");
    do
    {
        
        while ( !Serial.available() ); 
        inByte = Serial.read(); 
        longitude[i]=inByte;// reading a character from the GPS
        i++;
        //Serial.write ( inByte );
        //Serial.write(longitude);// printing the Longitude
    } while ( ',' != inByte );
    i--;
    longitude[i]='\0';
    //Serial.write(longitude);
//============== printing the east cordinate ===============//


//Serial.println(latitude);
//Serial.println(longitude);

//Latitude
sscanf(latitude,"%f",&lat);
latdeg=lat/100;
latmin=lat-(latdeg*100);
lat=latdeg+(latmin/60);
sprintf(latitude,"%f",lat);
Serial.print("Latitude:");
Serial.println(latitude);

//Longitude
sscanf(longitude,"%f",&lon);
londeg=lon/100;
lonmin=lon-(londeg*100);
lon=londeg+(lonmin/60);
sprintf(longitude,"%f",lon);
Serial.print("Longitude:");
Serial.println(longitude);

sprintf(link2,"%s,%s",latitude,longitude);
sprintf(link,"%s%s",link1,link2);
Serial.println(link);

//Serial.begin(9600);
  configTime(0, 0, "pool.ntp.org");      
  client.setTrustAnchors(&cert);

  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  int a = 0;
  while (WiFi.status() != WL_CONNECTED) {
    Serial.print(".");
    delay(500);
    a++;
  }
  


  Serial.println("");
  Serial.println("WiFi connected");
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
  bot.sendMessage(CHAT_ID, "garbage is filled plz visit the location soon");  // THIS LINE IS USED SEND THE MESSEGE
  bot.sendMessage(CHAT_ID, link);
  Serial.println("MSG SENT");
}

void loop() 
{
  digitalWrite(trig,1);
  delayMicroseconds(10);
  digitalWrite(trig,0);
  duration = pulseIn(echo,1);
  distance = duration*0.034/2;
  Serial.println(distance);
  if(distance<=8)
  {
  digitalWrite(buz,1);
  digitalWrite(led,1);
  gps();
  Serial.print("garbage filled\n");
  Serial.print(distance);
  
  Serial.print("\n");
  delay(500);
  }
  else
  {
    
    Serial.println("actual distance measured\n");
    Serial.print(distance);
    digitalWrite(buz,0);
    digitalWrite(led,0);
    Serial.print("\n");
    delay(500);
  }

 
}

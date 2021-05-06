
#include "time.h"
#include <WiFi.h>
#include <WebServer.h>
#include <OneWire.h>
#include <DallasTemperature.h>

/*set the key parameters */
// set date and time for switching
const int onhour  = 10;
const int offhour = 11;
const int onmin = 01 ;
const int offmin = 01 ;
const int EVENDATES = 0;

// GPIO where the DS18B20 is connected to
const int oneWireBus = 2;  
// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(oneWireBus);
// Pass our oneWire reference to Dallas Temperature sensor 
DallasTemperature sensors(&oneWire);

int switchStatus = 0 ;               // status switch
boolean pompStatus = false ;

int switchPin = 4;              // GPIO4 or D2
int timeAlert ;
int pompOn = 0;

// Pin settings:
const int ledPin = 5 ;              // GPIO5 or D1
const int relaisPin = 14 ;          // GPIO16

// internet connection 
const char* ssid = "Dorskamp";
const char* password = "46498342";

const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = 3600;
const int   daylightOffset_sec = 3600;

WebServer server(80);

int nhour;
int nminute;
int nday;

bool zkstatus = false;
int returncode = 404 ;
struct tm timeinfo;

void getTime()
 {
  //struct tm timeinfo;
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  if(!getLocalTime(&timeinfo)){
    Serial.println("Failed to obtain time");
    return;
    }
  }


// setup the system
void setup() {
  Serial.begin(115200);
  delay(100);

  // Start the DS18B20 sensor
  sensors.begin();
  
  // set the digital pin as output:
  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  pinMode(relaisPin, OUTPUT);
  digitalWrite(relaisPin, LOW);

  
// connect to dorskamp using a fixed iP
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);
  IPAddress ip(192,168,1,142);   
  IPAddress gateway(192,168,1,254);   
  IPAddress dns(8,8,8,8);  
  IPAddress subnet(255,255,255,0);   
  WiFi.config(ip, gateway, subnet, dns);
  int connectcount = 0;

  //check wi-fi is connected to wi-fi network if not stop the program
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    connectcount = connectcount + 1 ;
    Serial.print(".");
    if (connectcount == 50) {
      //stop after 15 attempts to connect
      stop();
   }
  }
  
  //connected
  Serial.println("");
  Serial.println("WiFi connected..!");
  Serial.print("Got IP: ");  Serial.println(WiFi.localIP());
  
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  getTime();
  Serial.println(&timeinfo, "%A, %B %d %Y %H:%M:%S");

  
  //identify instructions and actions
  server.on("/", handle_onconnect);
  server.on("/status", handle_status);
  server.on("/pompaan", handle_paan);
  server.on("/pompuit", handle_puit);
  server.on("/temp", handle_temp);
  server.onNotFound(handle_NotFound);
  
  //start the webserver 
  server.begin();
  Serial.println("HTTP server started");
}

// run the program
void loop() {

  //listen an handle given instruction
  server.handleClient();

  switchStatus = digitalRead(switchPin);   // read status of switch
  //digitalWrite(ledPin, switchStatus); 
  //digitalWrite(relaisPin, switchStatus); 

  if (!getLocalTime(&timeinfo)){
    Serial.println("Failed to obtain time");
    return;
  }
   
  // Serial.println(&timeinfo, "%A, %B %d %Y %H:%M:%S");
  
  nhour = timeinfo.tm_hour;
  nminute = timeinfo.tm_min;
  nday = timeinfo.tm_mday;
  // delay(1000);
  
  /* is this an even day ? if so run opump */
  if ( ((nday % 2) == EVENDATES) || switchStatus == 1  )
     {
       if(nhour == onhour && nminute == onmin ){
       // set the LED with the ledState of the variable:
         timeAlert = 1; 
     } // timeron

      if(nhour == offhour && nminute == offmin ){
      // set the LED with the ledState of the variable:
         timeAlert = 0; 
      } //timeroff
     } // evendayd

     if( (timeAlert == 1) || switchStatus == 1 || pompStatus){
      digitalWrite(ledPin, HIGH);
      digitalWrite(relaisPin, HIGH);
       } else {
      digitalWrite(ledPin, LOW);
      digitalWrite(relaisPin, LOW);
     }
 
  }  



//functions responding on webserver instructions

void handle_status() {
  Serial.println("Status");
  returncode = 203;
  server.send(returncode, "text/plain", "oke" ); 
}

void handle_onconnect() {
  returncode = 203;
  Serial.println("Connected");
  server.send(returncode, "text/html", SendHTML(true, 202 )); 
}

void handle_temp() {
  Serial.println("Wat is de temperatuur ");
  sensors.requestTemperatures(); 
  float temp = sensors.getTempCByIndex(0);
  Serial.print(temp);
  Serial.println(" C");

  returncode = 203;
  server.send(returncode, "text/plain", String(temp) ); 
  
}

void handle_NotFound(){
  server.send(404, "text/plain", "Instruction Not found");
}

void handle_paan(){
  server.send(203, "text/plain", "Pomp Aan");
  Serial.println("Pomp Aan");
  pompStatus = true ;
  
}

void handle_puit(){
  server.send(203, "text/plain", "Pomp Uit");
  Serial.println("Pomp Uit");
  pompStatus = false ;
  
}



void stop(){
 while(1){
      Serial.println("Failed to connect");
      digitalWrite(ledPin,HIGH);
      delay(100);
      digitalWrite(ledPin,LOW);
      delay(100);
 }
}


void blink_oke(){
      digitalWrite(ledPin,HIGH);
      delay(1000);
      digitalWrite(ledPin,LOW);
      delay(1000);
      digitalWrite(ledPin,HIGH);
      delay(1000);
      digitalWrite(ledPin,LOW);
}

void blink_error(){
      digitalWrite(ledPin,HIGH);
      delay(1000);
      digitalWrite(ledPin,LOW);
      delay(100);
      digitalWrite(ledPin,HIGH);
      delay(1000);
      digitalWrite(ledPin,LOW);
}

String SendHTML(uint8_t led1stat,uint8_t led2stat){
  String ptr = "<!DOCTYPE html> <html>\n";
  ptr +="<head><meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0, user-scalable=no\">\n";
  ptr +="<title>Sproeier Control</title>\n";
  ptr +="<style>html { font-family: Helvetica; display: inline-block; margin: 0px auto; text-align: center;}\n";
  ptr +="body{margin-top: 50px;} h1 {color: #444444;margin: 50px auto 30px;} h3 {color: #444444;margin-bottom: 50px;}\n";
  ptr +=".button {display: block;width: 80px;background-color: #3498db;border: none;color: white;padding: 13px 30px;text-decoration: none;font-size: 25px;margin: 0px auto 35px;cursor: pointer;border-radius: 4px;}\n";
  ptr +=".button-on {background-color: #3498db;}\n";
  ptr +=".button-on:active {background-color: #2980b9;}\n";
  ptr +=".button-off {background-color: #34495e;}\n";
  ptr +=".button-off:active {background-color: #2c3e50;}\n";
  ptr +="p {font-size: 14px;color: #888;margin-bottom: 10px;}\n";
  ptr +="</style>\n";
  ptr +="</head>\n";
  ptr +="<body>\n";
  ptr +="<h1>ESP32 Pool Control + temperature Sensor</h1>\n";
  ptr +="<h3>Listening to your commands</h3>\n";
  
 /* if(tkstatus)
  {ptr +="<p>Tuin Klep Status: ON</p><a class=\"button button-off\" href=\"/zwembadoff\">OFF</a>\n";}
  else
  {ptr +="<p>LED1 Status: OFF</p><a class=\"button button-on\" href=\"/zwembadon\">ON</a>\n";}

  if(zkstatus)
  {ptr +="<p>LED2 Status: ON</p><a class=\"button button-off\" href=\"/tuinoff\">OFF</a>\n";}
  else
  {ptr +="<p>LED2 Status: OFF</p><a class=\"button button-on\" href=\"/tuinon\">ON</a>\n";}

  ptr +="</body>\n";
  ptr +="</html>\n";
  */
  
  return ptr;
}

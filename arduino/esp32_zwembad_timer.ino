#include "time.h"
#include <WiFi.h>
#include <WebServer.h>

#include <OneWire.h>
#include <DallasTemperature.h>

/*set the key parameters */
// set date and time for switching
const int onhour  = 12;
const int offhour = 13;
const int onmin = 01 ;
const int offmin = 01 ;
const int EVENDATES = 0;

// GPIO where the DS18B20 is connected to
const int oneWireBus = 2;  
// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(oneWireBus);
// Pass our oneWire reference to Dallas Temperature sensor 
DallasTemperature sensors(&oneWire);

boolean pompStatus = false ;
boolean timeAlert = false ;


// Pin settings:
const int ledPin = 18 ;
const int relaisPin = 14 ;

// internet connection 
const char* ssid = "Dorskamp";
const char* password = "46498342";

// timer variables
const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = 3600;
const int   daylightOffset_sec = 3600;
struct tm timeinfo;

int nhour;
int nminute;
int nday;

//webserver interaction
int returncode = 404 ;


WebServer server(80);

void connectNetwork()
{
  int connectcount = 0;
  
  IPAddress ip(192,168,1,142);   
  IPAddress gateway(192,168,1,254);   
  IPAddress subnet(255,255,255,0);
  IPAddress dns(8,8,8,8);  
  WiFi.config(ip, gateway, subnet,dns);

  // connect to dorskamp using a fixed iP
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  //start wi-fi check connection to wi-fi network if reconnect
  while (WiFi.begin(ssid, password) != WL_CONNECTED) {
      delay(10000);
  
      connectcount = connectcount + 1 ;
      if (connectcount == 100 ) {
      //stop after 100 attempts to connect
          delay(60000);
          connectcount = 0 ;
      }
       Serial.print('.');
  }
  Serial.println("WiFi connected..!");
  Serial.print("Got IP: ");  Serial.println(WiFi.localIP());
}

//get the global time and place this in struct timeinfo for use during in the loop
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

  //connect to the wifio network
  connectNetwork();
  
  //start the webserver 
  server.begin();
  Serial.println("HTTP server started");
  
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
}

// run the program
void loop() {
  
  //are we still conected?
  if (WiFi.status() != WL_CONNECTED ) {
    // not connected -> connect again
    Serial.println("HELP//SOS//DISCONNECED");
    Serial.println("initiate reconnection ");

    connectNetwork();
   }

   //listen an handle given instruction
   server.handleClient();

  if (!getLocalTime(&timeinfo)){
    Serial.println("Failed to obtain time");
    return;
  }
   
  // Serial.println(&timeinfo, "%A, %B %d %Y %H:%M:%S");
  
  nhour = timeinfo.tm_hour;
  nminute = timeinfo.tm_min;
  nday = timeinfo.tm_mday;
  
  /* is this an even day ? if so run opump */
  if ( ((nday % 2) == EVENDATES)  )
     {
       if(nhour == onhour && nminute == onmin ){
       // set the LED with the ledState of the variable:
         timeAlert = true; 
     } // timeron

      if(nhour == offhour && nminute == offmin ){
      // set the LED with the ledState of the variable:
         timeAlert = false; 
      } //timeroff  
     } // evendayd

   if( timeAlert  || pompStatus){
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
  String statustekst = " "  ;
  
  if (pompStatus) { statustekst = "Filterpomp on "; } else { statustekst = "Filterpomp off "; }
  returncode = 203;
  server.send(returncode, "text/plain", statustekst ); 
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
 
  return ptr;
  }

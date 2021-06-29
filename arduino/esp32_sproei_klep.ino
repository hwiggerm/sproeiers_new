#include <WiFi.h>
#include <WebServer.h>
#include "time.h"

// internet connection 
const char* ssid = "Dorskamp";
const char* password = "46498342";

const char* ntpServer = "pool.ntp.org";
const long  gmtOffset_sec = 3600;
const int   daylightOffset_sec = 3600;

struct tm timeinfo;
int nsec;
int timeOke = 1;

int connectError = 0 ;
WebServer server(80);

void getTime()
 {
  //struct tm timeinfo;
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  if(!getLocalTime(&timeinfo)){
    Serial.println("Failed to obtain time");
    return;
    }
  }


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

// GPIO Pins 21/22/23 
#define ONBOARD_LED  2
uint8_t zwembad_klep_pin = 23;
bool zkstatus = false;

uint8_t tuin_klep_pin = 22;
bool tkstatus = true;

uint8_t power_pin = 21;
bool pwrstatus = true;


int returncode = 404 ;

// setup the system
void setup() {
  Serial.begin(115200);

  delay(100);
  pinMode(zwembad_klep_pin, OUTPUT);
  pinMode(tuin_klep_pin, OUTPUT);
  pinMode(power_pin, OUTPUT);
  pinMode(ONBOARD_LED, OUTPUT);


  //connect to the wifio network
  connectNetwork();
  
  configTime(gmtOffset_sec, daylightOffset_sec, ntpServer);
  getTime();
  Serial.println(&timeinfo, "%A, %B %d %Y %H:%M:%S");

  // check power and kleppen
  voeding_aan();

  //play sequence to check the components
  zwembadklep_aan();
  delay(2000);
  zwembadklep_uit();
  delay(2000);
  
  tuinklep_aan();
  delay(2000);
  tuinklep_uit();
  delay(2000);

  voeding_uit();


 //identify instructions and actions
  server.on("/", handle_onconnect);
  server.on("/status", handle_status);
  server.on("/zwembadon", handle_zwembadklep_on);
  server.on("/tuinon", handle_tuinklep_on);
  server.on("/poweroff", handle_power_off);
  server.onNotFound(handle_NotFound);
  
  //start the webserver 
  server.begin();
  Serial.println("HTTP server started");
}

// run the program
void loop() {
 
  //are we still conected?
  if (WiFi.status() != 3 ) {
    Serial.println("HELP//SOS//DISCONNECED");
    Serial.println("initiate reconnection ");

    connectNetwork();
   }

  //listen an handle given instruction
  server.handleClient();

  //only set kleppen when power is on
  if(pwrstatus)
  { 
      //always switch/leve power on (to be sure) untill swithched off
      digitalWrite(power_pin, HIGH);
      delay(1000);
      returncode = 203;

    if(zkstatus)
    //zwembad
    //when true; flip zwembad on and 1 sec later tuin off if not flip tuin on and zwembad off
    { 
      digitalWrite(zwembad_klep_pin, HIGH);
      returncode = 202;
      digitalWrite(tuin_klep_pin, LOW);
    }
    else
    { 
      digitalWrite(tuin_klep_pin, HIGH);
      returncode = 201;
      digitalWrite(zwembad_klep_pin, LOW);
    }
    //tuin 
    //when true; flip tuin on and 1 sec later zwembad off if not flip zwembad on and tuin off
    if(tkstatus)
      {
        digitalWrite(tuin_klep_pin, HIGH);
        returncode = 201;
        digitalWrite(zwembad_klep_pin, LOW);
      }
    else
      {
        digitalWrite(zwembad_klep_pin, HIGH);
        returncode = 202;
        digitalWrite(tuin_klep_pin, LOW);
      }
  }

  else

  //keep power low as we are on powerdown
  { 
    digitalWrite(power_pin, LOW);
    returncode = 203;
  }
}



//functions responding on webserver instructions

void handle_status() {
  Serial.println("Status");
  String statustekst = " "  ;
  
  if (pwrstatus) { statustekst = "Power on "; } else { statustekst = "Power off "; }
  if (zkstatus) { statustekst = statustekst + "Connect errors " + String(connectError) + " - zwembad klep on" ; }
  if (tkstatus) { statustekst = statustekst + "Connect errors " + String(connectError) + " - tuinklep on" ; }
 
  returncode = 203;
  server.send(returncode, "text/plain", statustekst ); 
}

void handle_onconnect() {
  Serial.println("Connected");
  server.send(returncode, "text/html", SendHTML(true, pwrstatus )); 
}

void handle_zwembadklep_on() {
  pwrstatus = true ;
  zkstatus = true ;
  tkstatus = false ;

  Serial.println("Zwembadklep Status: ON");
  server.send(returncode, "text/html", SendHTML(true,zkstatus)); 
}

void handle_tuinklep_on() {
  pwrstatus = true ;
  tkstatus = true;
  zkstatus = false ;

  Serial.println("Tuinklep Status: ON");
  // server.send(200, "text/html", SendHTML(true,tkstatus)); 
  server.send(returncode, "text/html", SendHTML(true,'Tuinklep')); 
}

void handle_power_on(){
  pwrstatus = true;
  Serial.println("Power: ON");
  server.send(returncode, "text/html", SendHTML(true,pwrstatus)); 
}

void handle_power_off(){
  digitalWrite(power_pin,LOW);
  digitalWrite(tuin_klep_pin,LOW);
  digitalWrite(zwembad_klep_pin,LOW);
  
  pwrstatus = false ;
  tkstatus = true ;
  zkstatus = false ;
  
  Serial.println("Power: OFF");
  server.send(returncode, "text/html", SendHTML(true,pwrstatus)); 
}

void handle_NotFound(){
  server.send(404, "text/plain", "Instruction Not found");
}

void stop(){
 while(1){
      digitalWrite(ONBOARD_LED,HIGH);
      delay(100);
      digitalWrite(ONBOARD_LED,LOW);
      delay(100);
 }
}

void voeding_aan(){
  digitalWrite(power_pin,HIGH);
  Serial.println("voeding : ON");
}

void voeding_uit(){
  digitalWrite(power_pin,LOW);
  Serial.println("voeding : OFF");
}

void tuinklep_aan(){
  digitalWrite(tuin_klep_pin,HIGH);
  Serial.println("tuinklep : ON");
}

void tuinklep_uit(){
  digitalWrite(tuin_klep_pin,LOW);
  Serial.println("tuinklep : OFF");
}

void zwembadklep_aan(){
  digitalWrite(zwembad_klep_pin,HIGH);
  Serial.println("zwembadklep : ON");
}

void zwembadklep_uit(){
  digitalWrite(zwembad_klep_pin,LOW);
  Serial.println("zwembadklep : OFF");
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
  ptr +="<h1>ESP32 Sprinkler Control</h1>\n";
  ptr +="<h3>Listening to your commands</h3>\n";
  
  return ptr;
}

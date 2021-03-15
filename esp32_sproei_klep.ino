
#include <WiFi.h>
#include <WebServer.h>

#define ONBOARD_LED  2


/*
https://lastminuteengineers.com/creating-esp32-web-server-arduino-ide/
*/

/*Put your SSID & Password*/
const char* ssid = "Dorskamp";
const char* password = "46498342";

WebServer server(80);

uint8_t zwembad_klep_pin = 23;
bool zkstatus = LOW;

uint8_t tuin_klep_pin = 22;
bool tkstatus = LOW;

uint8_t power_pin = 21;
bool pwrstatus = LOW;

void setup() {
  Serial.begin(115200);

  delay(100);
  pinMode(zwembad_klep_pin, OUTPUT);
  pinMode(tuin_klep_pin, OUTPUT);
  pinMode(power_pin, OUTPUT);
  pinMode(ONBOARD_LED, OUTPUT);
  
  Serial.println("Connecting to ");
  Serial.println(ssid);

  //connect to your local wi-fi network
  WiFi.begin(ssid, password);
  IPAddress ip(10,0,0,141);   
  IPAddress gateway(10,0,0,1);   
  IPAddress subnet(255,255,255,0);   
  WiFi.config(ip, gateway, subnet);
  int connectcount = 0;

  //check wi-fi is connected to wi-fi network
  while (WiFi.status() != WL_CONNECTED) {
  delay(1000);
  
  connectcount = connectcount + 1 ;
   if (connectcount == 10) {
      /* na 10 poningen geven we verbindingen op */
      stop();
   }
  
  }
  
  Serial.println("");
  Serial.println("WiFi connected..!");
  Serial.print("Got IP: ");  Serial.println(WiFi.localIP());

  /* test de voeding en de kleppen */
  voeding_aan();

  zwembadklep_aan();
  delay(2000);
  zwembadklep_uit();
  delay(2000);
  
  tuinklep_aan();
  delay(2000);
  tuinklep_uit();
  delay(2000);

  voeding_uit();

  blink_oke();

  server.on("/", handle_onconnect);
  server.on("/zwembadon", handle_zwembadklep_on);
  server.on("/tuinon", handle_tuinklep_on);
  server.on("/poweroff", handle_power_off);
  
  server.onNotFound(handle_NotFound);
  
  server.begin();
  Serial.println("HTTP server started");
}


void loop() {
  server.handleClient();
  /*code responinf on requests*/
  if(zkstatus)
  { 
    voeding_aan()
    digitalWrite(zwembad_klep_pin, HIGH);
    digitalWrite(tuin_klep_pin, LOW);
  }
  else
  { 
    voeding_aan()
    digitalWrite(zwembad_klep_pin, LOW);
    digitalWrite(tuin_klep_pin, HIGH);
  }
  
  if(tkstatus)
  {
    voeding_aan()
    digitalWrite(tuin_klep_pin, HIGH);
    digitalWrite(zwembad_klep_pin, LOW);
    }
  else
  {
    voeding_aan()
    digitalWrite(tuin_klep_pin, LOW);
    digitalWrite(zwembad_klep_pin, HIGH);
  }
}

void handle_onconnect() {
  Serial.println("Connected");
  server.send(200, "text/html", SendHTML(true, pwrstatus )); 
}

void handle_zwembadklep_on() {
  zkstatus = true ;
  Serial.println("Zwembadklep Status: ON");
  server.send(200, "text/html", SendHTML(true,zkstatus)); 
}

void handle_tuinklep_on() {
  tkstatus = true;
  Serial.println("Tuinklep Status: ON");
  server.send(200, "text/html", SendHTML(true,tkstatus)); 
}

void handle_power_on(){
  pwrstatus = true;
  Serial.println("Power: ON");
  server.send(200, "text/html", SendHTML(true,pwrstatus)); 
}

void handle_power_off(){
  pwrstatus = false;
  Serial.println("Power: OFF");
  server.send(200, "text/html", SendHTML(true,pwrstatus)); 
}

void handle_NotFound(){
  server.send(404, "text/plain", "Not found");
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
  delay(100)
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

void blink_oke(){
      digitalWrite(ONBOARD_LED,HIGH);
      delay(1000);
      digitalWrite(ONBOARD_LED,LOW);
      delay(1000);
      digitalWrite(ONBOARD_LED,HIGH);
      delay(1000);
      digitalWrite(ONBOARD_LED,LOW);
}

void blink_error(){
      digitalWrite(ONBOARD_LED,HIGH);
      delay(1000);
      digitalWrite(ONBOARD_LED,LOW);
      delay(100);
      digitalWrite(ONBOARD_LED,HIGH);
      delay(1000);
      digitalWrite(ONBOARD_LED,LOW);
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

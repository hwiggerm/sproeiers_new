
#include <WiFi.h>
#include <WebServer.h>




/*set the key parameters */

// internet connection 
const char* ssid = "xxxxx";
const char* password = "xxxxx";
WebServer server(80);


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
  
// connect to dorskamp using a fixed iP
  Serial.println("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);
  IPAddress ip(10,0,0,141);   
  IPAddress gateway(10,0,0,1);   
  IPAddress subnet(255,255,255,0);   
  WiFi.config(ip, gateway, subnet);
  int connectcount = 0;

  //check wi-fi is connected to wi-fi network if not stop the program
  while (WiFi.status() != WL_CONNECTED) {
  delay(1000);
  
  connectcount = connectcount + 1 ;
   if (connectcount == 10) {
      //stop after 10 attempts to connect
      stop();
   }
  
  }
  
  //connected
  Serial.println("");
  Serial.println("WiFi connected..!");
  Serial.print("Got IP: ");  Serial.println(WiFi.localIP());

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

  //confirm checks are done
  blink_oke();
  
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

  //listen an handle given instruction

  server.handleClient();
  // if (pwrstatus) { returncode = 205; }

  //only set kleppen when power is on
  if(pwrstatus)
  { 
    //always switch/leve power on (to be sure) untill swithched off
    digitalWrite(power_pin, HIGH);
    delay(1000);

    if(zkstatus)
    //zwembad
    //when true; flip zwembad on and 1 sec later tuin off if not flip tuin on and zwembad off
    { 
      digitalWrite(zwembad_klep_pin, HIGH);
      returncode = 202;
      delay(1000);
      digitalWrite(tuin_klep_pin, LOW);
    }
    else
    { 
      digitalWrite(tuin_klep_pin, HIGH);
      returncode = 201;
      delay(1000);
      digitalWrite(zwembad_klep_pin, LOW);
    }
    //tuin 
    //when true; flip tuin on and 1 sec later zwembad off if not flip zwembad on and tuin off
    if(tkstatus)
      {
        digitalWrite(tuin_klep_pin, HIGH);
        returncode = 201;
        delay(1000);
        digitalWrite(zwembad_klep_pin, LOW);
      }
    else
      {
        digitalWrite(zwembad_klep_pin, HIGH);
        returncode = 202;
        delay(1000);
        digitalWrite(tuin_klep_pin, LOW);
      }
  }

  else

  //keep power low as we are on powerdown
  { 
    digitalWrite(power_pin, LOW);
    returncode = 203;
    delay(100);
  }
}

//functions responding on webserver instructions

void handle_status() {
  Serial.println("Status");
  server.send(returncode, "text/plain", "oke" ); 
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
  server.send(returncode, "text/html", SendHTML(true,tkstatus)); 
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
  tkstatus = false ;
  zkstatus = false ;
  
  returncode = 210
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
  delay(100);
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

void setup() { 
  pinMode(21, OUTPUT);
  pinMode(22, OUTPUT);
  pinMode(23, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  Serial.println("poort 21");
  digitalWrite(21, HIGH);
  delay(2000);
  Serial.println("poort 22");  
  digitalWrite(22, HIGH);
  delay(2000);
  Serial.println("poort 23");
  digitalWrite(23, HIGH);
  delay(4000);

  digitalWrite(21, LOW);
  digitalWrite(22, LOW);
  digitalWrite(23, LOW);
  delay(4000);


} 

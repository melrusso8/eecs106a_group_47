// the number of the LED pin
const int ledPin = 26;  // 16 corresponds to GPIO16

// setting PWM properties
const int freq = 5000;
const int ledChannel = 0;
const int resolution = 8;
 
void setup(){
  // configure LED PWM functionalitites
  ledcSetup(ledChannel, freq, resolution);
  
  // attach the channel to the GPIO to be controlled
  ledcAttachPin(ledPin, ledChannel);

  Serial.begin(9600);
  Serial.println("Speed 0 to 255");
}
 
void loop(){
  if (Serial.available()) {
      int speed = Serial.parseInt();
      if (speed >= 0 && speed <= 255) {
         ledcWrite(ledChannel, speed);
         Serial.print("Running at ");
         Serial.println(speed);
         delay(100);
         ledcWrite(ledChannel, 0);
      }
   }
}

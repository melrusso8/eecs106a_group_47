#include <WiFi.h>// ESP32 WiFi include
#include <HCSR04.h>
#define ONBOARD_LED 13
#define trigPin 27
#define echoPin 34
UltraSonicDistanceSensor distanceSensor(trigPin, echoPin);
float previous_val;
float current_val;
float tolerance = 0.2;
byte counterEmptyMax = 10;
byte counterEmpty = 0;
byte counterFullMax = 10;
byte counterFull = 0;
bool empty = false;


const uint ServerPort = 8088;
/*Create a server and listen on ServerPort */
WiFiServer Server(ServerPort);

// the number of the motor pin
const int motorPin = 26;  

// setting PWM properties
const int freq = 5000;
const int ledChannel = 0;
const int resolution = 8;

void setup() {
  pinMode(ONBOARD_LED,OUTPUT);
   // configure LED PWM functionalitites
  ledcSetup(ledChannel, freq, resolution);
  
  // attach the channel to the GPIO to be controlled
  ledcAttachPin(motorPin, ledChannel);
  Serial.begin(9600);
  ConnectToWiFi();
  Server.begin();
}

void loop() {
    /* listen for client */
    WiFiClient client = Server.available(); 
    uint8_t data[30];
    current_val = distanceSensor.measureDistanceCm();
    if (abs(current_val - previous_val) > tolerance || current_val == -1) {
      if (counterFull > counterFullMax) {
        empty = false;
        counterFull = 0;
      }
      counterFull++;
    }
    else {
      if (counterEmpty > counterEmptyMax) {
        empty = true;
        counterEmpty = 0;
      }
      counterEmpty++;
    }
    previous_val = current_val;
    if (client) {                   
      Serial.println("new client");
      flashLed();     
      /* check client is connected */           
      while (client.connected()) {          
          if (client.available()) {
              int len = client.read(data, 30);
              if(len < 30){
                  data[len] = '\0';  
              }else {
                  data[30] = '\0';
              }    
              if(data[0] == 'y') {
                Serial.println("Distribute seed!");
                ledcWrite(ledChannel, 255);
                delay(1000);
                ledcWrite(ledChannel, 0);
                client.println("z");
              }
              if (empty) {
                client.println("Empty!");
              } else {
                client.println("False!");
              }
          }
          
      } 
    }
    delay(100);
}

void ConnectToWiFi()
{
 
  WiFi.mode(WIFI_STA);
  WiFi.begin("Polly", "");
  Serial.print("Connecting to "); Serial.println("");
 
  uint8_t i = 0;
  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print('.');
    delay(500);
 
    if ((++i % 16) == 0)
    {
      Serial.println(F(" still trying to connect"));
    }
  }
  Serial.print(F("Connected. My IP address is: "));
  Serial.println(WiFi.localIP());
  Serial.print("RRSI: ");
  Serial.println(WiFi.RSSI());
  flashLed();
}

void flashLed() {
  for(int i = 0; i < 5;i++) {
    digitalWrite(ONBOARD_LED,HIGH);
    delay(200);
    digitalWrite(ONBOARD_LED,LOW);
    delay(200);
  }
}

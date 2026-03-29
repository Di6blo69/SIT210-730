#include <Wire.h>
#include <BH1750.h>


#define PIR_PIN 2
#define SWITCH_PIN 3
#define LED1 5
#define LED2 6

BH1750 lightMeter;


volatile bool motionFlag = false;
volatile bool switchFlag = false;

void setup() {
  Serial.begin(9600);

  pinMode(PIR_PIN, INPUT);
  pinMode(SWITCH_PIN, INPUT);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);

  Wire.begin();

  
  if (lightMeter.begin()) {
    Serial.println("Light sensor ready");
  } else {
    Serial.println("Light sensor error");
  }

  
  attachInterrupt(digitalPinToInterrupt(PIR_PIN), motionISR, RISING);
  attachInterrupt(digitalPinToInterrupt(SWITCH_PIN), switchISR, CHANGE);
}

void loop() {
  float lightLevel = lightMeter.readLightLevel();

  Serial.print("Light: ");
  Serial.println(lightLevel);

  
  if (motionFlag) {
    Serial.println("Motion detected!");

    if (lightLevel < 10) {   
      turnLightsOn();
      Serial.println("Lights ON (dark)");
    } else {
      turnLightsOff();
      Serial.println("Lights OFF (bright)");
    }

    motionFlag = false;
  }

  
  if (switchFlag) {
    Serial.println("Switch activated!");
    turnLightsOn();
    Serial.println("Lights ON (manual)");

    switchFlag = false;
  }

  
  if (lightLevel >= 10) {
    turnLightsOff();
  }

  delay(300);
}


void motionISR() {
  motionFlag = true;
}

void switchISR() {
  switchFlag = true;
}


void turnLightsOn() {
  digitalWrite(LED1, HIGH);
  digitalWrite(LED2, HIGH);
}


void turnLightsOff() {
  digitalWrite(LED1, LOW);
  digitalWrite(LED2, LOW);
}
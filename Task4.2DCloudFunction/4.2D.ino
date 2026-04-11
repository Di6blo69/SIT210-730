#include "thingProperties.h"

const int livingRoomLED = 3;
const int bathroomLED = 4;
const int closetLED = 5;

bool livingState = false;
bool bathroomState = false;
bool closetState = false;

void setup() {
  Serial.begin(9600);
  delay(1500);

  pinMode(livingRoomLED, OUTPUT);
  pinMode(bathroomLED, OUTPUT);
  pinMode(closetLED, OUTPUT);

  digitalWrite(livingRoomLED, LOW);
  digitalWrite(bathroomLED, LOW);
  digitalWrite(closetLED, LOW);

  initProperties();
  ArduinoCloud.begin(ArduinoIoTPreferredConnection);

  setDebugMessageLevel(2);
  ArduinoCloud.printDebugInfo();
}

void loop() {
  ArduinoCloud.update();
}

void onRoomCommandChange() {
  String room = roomCommand;
  room.toLowerCase();

  if (room == "living room") {
    livingState = !livingState;
    digitalWrite(livingRoomLED, livingState ? HIGH : LOW);
    Serial.println("Living room toggled");
  }
  else if (room == "bathroom") {
    bathroomState = !bathroomState;
    digitalWrite(bathroomLED, bathroomState ? HIGH : LOW);
    Serial.println("Bathroom toggled");
  }
  else if (room == "closet") {
    closetState = !closetState;
    digitalWrite(closetLED, closetState ? HIGH : LOW);
    Serial.println("Closet toggled");
  }
  else {
    Serial.println("Invalid room name");
  }
}
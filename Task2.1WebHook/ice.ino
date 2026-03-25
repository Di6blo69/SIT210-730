#include <WiFiNINA.h>
#include <ThingSpeak.h>
#include "function.h"
#include "secrets.h"

WiFiClient client;

unsigned long channelID = 3312197;
const char *apiKey = "DNCIXLBD9F31CT76";

void setup()
{
  Serial.begin(9600);

  initSensors();

  Serial.print("Connecting...");
  WiFi.begin(SECRET_SSID, SECRET_PASS);

  while (WiFi.status() != WL_CONNECTED)
  {
    delay(1000);
    Serial.print(".");
  }

  Serial.println("Connected!");

  ThingSpeak.begin(client);
}

void loop()
{
  float temp = readTemperature();
  float light = readLight();

  Serial.print("Temp: ");
  Serial.print(temp);
  Serial.print(" | Light (%): ");
  Serial.println(light);

  ThingSpeak.setField(1, temp);
  ThingSpeak.setField(2, light);

  int status = ThingSpeak.writeFields(channelID, apiKey);

  Serial.print("Status: ");
  Serial.println(status);

  delay(30000);
}
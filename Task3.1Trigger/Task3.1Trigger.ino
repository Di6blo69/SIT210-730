#include <WiFiNINA.h>
#include <Wire.h>
#include <BH1750.h>

char ssid[] = "RicardoMilos"; 
char pass[] = "blablabla";

const char* host = "maker.ifttt.com";
String key = "dQYL4ClsCuguswV-XWtqZm";

// IFTTT event names
String sunlightOnEvent = "sunlight_started";
String sunlightOffEvent = "sunlight_stopped";

WiFiClient client;
BH1750 lightMeter;


float lightThreshold = 300.0;


bool sunlightDetected = false;

void connectWiFi() {
  Serial.print("Connecting to WiFi");

  while (WiFi.begin(ssid, pass) != WL_CONNECTED) {
    Serial.print(".");
    delay(2000);
  }

  Serial.println();
  Serial.println("Connected to WiFi!");
}

void sendIFTTTEvent(String eventName, String value1) {
  if (client.connect(host, 80)) {
    String url = "/trigger/" + eventName + "/with/key/" + key + "?value1=" + value1;

    client.println("GET " + url + " HTTP/1.1");
    client.println("Host: maker.ifttt.com");
    client.println("Connection: close");
    client.println();

    Serial.print("Notification sent: ");
    Serial.println(eventName);
  } else {
    Serial.println("Connection to IFTTT failed");
  }

  delay(1000);
  while (client.available()) {
    client.read();
  }
  client.stop();
}

void setup() {
  Serial.begin(9600);
  delay(2000);

  Wire.begin();

  if (lightMeter.begin()) {
    Serial.println("BH1750 started successfully");
  } else {
    Serial.println("Error starting BH1750");
    while (1);
  }

  connectWiFi();
}

void loop() {
  float lux = lightMeter.readLightLevel();

  Serial.print("Light: ");
  Serial.print(lux);
  Serial.println(" lx");

  // Sunlight started
  if (lux > lightThreshold && sunlightDetected == false) {
    sunlightDetected = true;
    sendIFTTTEvent(sunlightOnEvent, "Sunlight started. Lux = " + String(lux));
  }

  // Sunlight stopped
  else if (lux <= lightThreshold && sunlightDetected == true) {
    sunlightDetected = false;
    sendIFTTTEvent(sunlightOffEvent, "Sunlight stopped. Lux = " + String(lux));
  }

  delay(3000);
}
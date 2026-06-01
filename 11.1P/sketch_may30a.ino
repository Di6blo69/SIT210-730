#include <SPI.h>
#include <WiFiNINA.h>
#include <Wire.h>
#include <DHT.h>

#define SECRET_SSID "Telstra272246"
#define SECRET_PASS "49t7kxadt6"

const int ledPin = 5;
const int buttonPin = 2;
const int buzzerPin = 4;
const int pirPin = 3;

#define DHTPIN 7
#define DHTTYPE DHT22
DHT dht(DHTPIN, DHTTYPE);

char server[] = "192.168.0.236";
int port = 5000;

WiFiClient client;

unsigned long lastSendTime = 0;
const unsigned long sendInterval = 1000;

String patientID = "patient1";

// BH1750
const byte BH1750_ADDR = 0x23;
float darkThreshold = 20.0;   // change this if needed

void bh1750Begin() {
  Wire.beginTransmission(BH1750_ADDR);
  Wire.write(0x01); // power on
  Wire.endTransmission();

  delay(10);

  Wire.beginTransmission(BH1750_ADDR);
  Wire.write(0x10); // continuous high resolution mode
  Wire.endTransmission();

  delay(180);
}

float readBH1750Lux() {
  if (Wire.requestFrom(BH1750_ADDR, 2) == 2) {
    uint16_t raw = (Wire.read() << 8) | Wire.read();
    float lux = raw / 1.2;
    return lux;
  }
  return -1;
}

void setup() {
  Serial.begin(9600);

  pinMode(ledPin, OUTPUT);
  pinMode(buttonPin, INPUT_PULLUP);
  pinMode(pirPin, INPUT);

  Wire.begin();
  bh1750Begin();
  dht.begin();

  Serial.println("Connecting to WiFi...");
  while (WiFi.begin(SECRET_SSID, SECRET_PASS) != WL_CONNECTED) {
    Serial.println("WiFi retry...");
    delay(2000);
  }

  Serial.println("WiFi connected");
  Serial.print("Nano IP: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  int buttonRaw = digitalRead(buttonPin);
  int motionState = digitalRead(pirPin);
  int buttonPressed = (buttonRaw == LOW) ? 1 : 0;

  float temp = dht.readTemperature();
  float hum = dht.readHumidity();
  float lux = readBH1750Lux();

  int isDark = 0;
  String lightStatus = "unknown";

  if (lux >= 0) {
    if (lux < darkThreshold) {
      isDark = 1;
      lightStatus = "dark";
    } else {
      isDark = 0;
      lightStatus = "bright";
    }
  }

  // Local safety logic
  if (buttonPressed == 1) {
    digitalWrite(ledPin, HIGH);
    tone(buzzerPin, 1000);
  } else {
    noTone(buzzerPin);

    if (motionState == HIGH && isDark == 1) {
      digitalWrite(ledPin, HIGH);
    } else {
      digitalWrite(ledPin, LOW);
    }
  }

  if (millis() - lastSendTime >= sendInterval) {
    lastSendTime = millis();

    if (client.connect(server, port)) {
      String jsonData = "{";
      jsonData += "\"patient_id\":\"" + patientID + "\",";
      jsonData += "\"button\":" + String(buttonPressed) + ",";
      jsonData += "\"motion\":" + String(motionState) + ",";
      jsonData += "\"led\":" + String(digitalRead(ledPin)) + ",";
      jsonData += "\"lux\":" + String(lux, 1) + ",";
      jsonData += "\"light_status\":\"" + lightStatus + "\",";

      if (!isnan(temp) && !isnan(hum)) {
        jsonData += "\"temp\":" + String(temp, 1) + ",";
        jsonData += "\"hum\":" + String(hum, 1);
      } else {
        jsonData += "\"temp\":null,";
        jsonData += "\"hum\":null";
      }

      jsonData += "}";

      client.println("POST /data HTTP/1.1");
      client.println("Host: 192.168.0.236");
      client.println("Content-Type: application/json");
      client.print("Content-Length: ");
      client.println(jsonData.length());
      client.println();
      client.println(jsonData);

      Serial.println("Sent: " + jsonData);
    } else {
      Serial.println("Connection to server failed");
    }

    client.stop();
  }

  delay(50);
}
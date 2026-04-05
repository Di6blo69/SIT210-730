#include <WiFiNINA.h>
#include <ArduinoMqttClient.h>


char ssid[] = "Telstra272246";
char pass[] = "49t7kxadt6";


const char broker[] = "broker.emqx.io";
int port = 1883;


const char waveTopic[] = "ES/Wave";
const char patTopic[]  = "ES/Pat";


#define TRIG_PIN 2
#define ECHO_PIN 3
#define LED1 5
#define LED2 6

WiFiClient wifiClient;
MqttClient mqttClient(wifiClient);


unsigned long lastDetectTime = 0;
const unsigned long detectCooldown = 1500; 

void setup() {
  Serial.begin(9600);
  while (!Serial);

  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);
  pinMode(LED1, OUTPUT);
  pinMode(LED2, OUTPUT);

  digitalWrite(LED1, LOW);
  digitalWrite(LED2, LOW);

  connectToWiFi();
  connectToMQTT();

  mqttClient.onMessage(onMqttMessage);

  mqttClient.subscribe(waveTopic);
  mqttClient.subscribe(patTopic);

  Serial.println("Subscribed to ES/Wave and ES/Pat");
}

void loop() {
  if (WiFi.status() != WL_CONNECTED) {
    connectToWiFi();
  }

  if (!mqttClient.connected()) {
    connectToMQTT();
    mqttClient.subscribe(waveTopic);
    mqttClient.subscribe(patTopic);
  }

  mqttClient.poll();

  float distance = readDistance();

  Serial.print("Distance: ");
  Serial.print(distance);
  Serial.println(" cm");

  unsigned long now = millis();

  
  if (distance > 10 && distance < 25 && (now - lastDetectTime > detectCooldown)) {
    publishWave();
    lastDetectTime = now;
  }

  
  else if (distance >= 1 && distance <= 10 && (now - lastDetectTime > detectCooldown)) {
    publishPat();
    lastDetectTime = now;
  }

  delay(200);
}

void connectToWiFi() {
  Serial.print("Connecting to WiFi");
  while (WiFi.begin(ssid, pass) != WL_CONNECTED) {
    Serial.print(".");
    delay(2000);
  }
  Serial.println();
  Serial.println("WiFi connected");
}

void connectToMQTT() {
  Serial.print("Connecting to MQTT broker... ");

  while (!mqttClient.connect(broker, port)) {
    Serial.print("Failed, error code = ");
    Serial.println(mqttClient.connectError());
    delay(2000);
  }

  Serial.println("connected");
}

float readDistance() {
  long duration;
  float distance;

  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  duration = pulseIn(ECHO_PIN, HIGH, 30000);

  if (duration == 0) {
    return 999; 
  }

  distance = duration * 0.0343 / 2.0;
  return distance;
}

void publishWave() {
  Serial.println("Wave detected -> Publishing to ES/Wave");

  mqttClient.beginMessage(waveTopic);
  mqttClient.print("SheronZ");
  mqttClient.endMessage();
}

void publishPat() {
  Serial.println("Pat detected -> Publishing to ES/Pat");

  mqttClient.beginMessage(patTopic);
  mqttClient.print("SheronZ");
  mqttClient.endMessage();
}

void onMqttMessage(int messageSize) {
  String topic = mqttClient.messageTopic();
  String message = "";

  while (mqttClient.available()) {
    message += (char)mqttClient.read();
  }

  Serial.print("Received on topic: ");
  Serial.println(topic);
  Serial.print("Message: ");
  Serial.println(message);

  if (topic == waveTopic) {
    digitalWrite(LED1, HIGH);
    digitalWrite(LED2, HIGH);
    Serial.println("Both LEDs ON");
  }
  else if (topic == patTopic) {
    digitalWrite(LED1, LOW);
    digitalWrite(LED2, LOW);
    Serial.println("Both LEDs OFF");
  }
}
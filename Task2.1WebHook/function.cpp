#include "function.h"
#include <Arduino.h>
#include <DHT.h>
#include <BH1750.h>
#include <Wire.h>

#define DHTPIN 2
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);
BH1750 lightMeter;

void initSensors()
{
  dht.begin();

  Wire.begin();          // start I2C
  lightMeter.begin();    // start BH1750
}

float readTemperature()
{
  return dht.readTemperature();
}

float readLight()
{
  return lightMeter.readLightLevel();  // returns lux
}
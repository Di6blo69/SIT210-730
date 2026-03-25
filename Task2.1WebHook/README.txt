# IoT Temperature and Light Monitoring System

## Description

This project uses an Arduino Nano 33 IoT to monitor temperature and ambient light levels. The system uses a DHT22 sensor for temperature and a BH1750 sensor for light intensity. Data is sent to ThingSpeak for real-time visualization.

## Features

* Reads temperature and light data
* Uses modular programming (function.cpp / function.h)
* Sends data to ThingSpeak via WiFi
* Displays real-time graphs

## Hardware Used

* Arduino Nano 33 IoT
* DHT22 Temperature Sensor
* BH1750 Light Sensor
* Breadboard & jumper wires

## Software Used

* Arduino IDE
* ThingSpeak

## How it Works

The Arduino reads sensor data and sends it to ThingSpeak every 30 seconds. The data is stored and displayed as graphs for monitoring.

## Security

WiFi credentials are stored in a separate `secrets.h` file for security.

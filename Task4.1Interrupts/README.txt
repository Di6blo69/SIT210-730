# Task 4.1P – Smart Lighting System Using Interrupts

## 📌 Project Overview

This project implements a smart lighting system using the Arduino Nano 33 IoT. The system automatically turns on lights when motion is detected in a dark environment and also allows manual control using a slider switch as a backup. The main objective of this task is to demonstrate the use of hardware interrupts to create a responsive and efficient embedded system.

---

## 🎯 Objectives

* Use hardware interrupts instead of polling
* Detect motion using a PIR sensor
* Measure ambient light using a BH1750 sensor
* Provide manual control using a slider switch
* Control two LEDs representing lights

---

## ⚙️ Hardware Components

* Arduino Nano 33 IoT
* PIR Motion Sensor
* BH1750 Light Sensor
* Slider Switch
* 2 × LEDs
* Resistors (220Ω for LEDs, 10kΩ for switch if using pull-down)
* Breadboard and jumper wires

---

## 🔌 Circuit Connections

| Component      | Connection |
| -------------- | ---------- |
| PIR Sensor OUT | D2         |
| Slider Switch  | D3         |
| LED 1          | D5         |
| LED 2          | D6         |
| BH1750 SDA     | SDA        |
| BH1750 SCL     | SCL        |
| Power          | 3.3V / 5V  |
| Ground         | GND        |

---

## 🧠 System Functionality

The system operates based on two main conditions:

1. **Automatic Mode (Motion + Darkness)**
   When motion is detected by the PIR sensor and the ambient light level is below a defined threshold, the LEDs are turned on automatically.

2. **Manual Mode (Switch Override)**
   If motion is not detected or the user prefers manual control, the slider switch can be used to turn on the lights.

Additionally, when the environment becomes bright, the system automatically turns off the LEDs to conserve energy.

---

## ⚡ Interrupt Implementation

Hardware interrupts are used to improve system responsiveness. Instead of continuously checking sensor values, the system reacts instantly when an event occurs.

* The PIR sensor triggers an interrupt when motion is detected.
* The slider switch triggers an interrupt when its state changes.

Interrupt Service Routines (ISR) are used to set flags, and the main loop processes these flags to control the system.

---

## 💻 Software Description

* The BH1750 sensor continuously provides light intensity values.
* Interrupt flags are used to detect motion and switch activation.
* LEDs are controlled based on sensor input and user interaction.
* The system ensures efficient operation by minimizing unnecessary processing.

---

## 🧪 Testing and Results

The system was tested under different conditions:

* In a dark environment, motion detection successfully turned on the LEDs.
* In a bright environment, the LEDs remained off or turned off automatically.
* The slider switch reliably activated the LEDs as a manual override.
* Serial Monitor outputs confirmed correct system behaviour.

---

## 🚀 Conclusion

This project demonstrates how hardware interrupts can be used to build a responsive and efficient embedded system. By combining motion detection, light sensing, and manual control, the system improves usability and energy efficiency. The use of interrupts reduces unnecessary processing and ensures immediate response to real-world events.

---


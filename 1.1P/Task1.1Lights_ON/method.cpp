#include "method.h"
#include <Arduino.h>

void turnOn(int LED1, int LED2, int time1, int time2, int B)
{
  if(digitalRead(B)>0)
  {
    digitalWrite(LED1,HIGH);
    digitalWrite(LED2,HIGH);
    delay(time1 *1000);
    digitalWrite(LED1,LOW);
    delay((time2- time1)*1000);
    digitalWrite(LED2,LOW);
    }
}
#include "method.h"

int B  = 12;
int LED1 = 13;
int LED2 = 11;
int time1 = 30;
int time2= 60;

void setup()
{
  pinMode(LED1, OUTPUT);
  pinMode(B,INPUT);
  pinMode(LED2, OUTPUT);
}

void loop()
{
  turnOn( LED1, LED2, time1, time2, B);
  
}
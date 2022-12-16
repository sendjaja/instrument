/*
Arduino 2x16 LCD - Detect Buttons
modified on 18 Feb 2019
by Saeed Hosseini @ Electropeak
https://electropeak.com/learn/
*/
#include <LiquidCrystal.h>
//LCD pin to Arduino
const int pin_RS = 8;
const int pin_EN = 9;
const int pin_d4 = 4;
const int pin_d5 = 5;
const int pin_d6 = 6;
const int pin_d7 = 7;
const int pin_BL = 10;
LiquidCrystal lcd( pin_RS,  pin_EN,  pin_d4,  pin_d5,  pin_d6,  pin_d7);

const int pin_PWR = A8;
const int pin_MEMBRANE_BTN = A13;
const int pin_MAG_INT = A14;
const int pin_MAG = A15;

int val = 0;

void setup() {
 lcd.begin(16, 2);
 lcd.setCursor(0,0);
 lcd.print("BLABLA");
 lcd.setCursor(0,1);
 lcd.print("Press Key:");

  pinMode(53, OUTPUT);
 pinMode(pin_PWR, OUTPUT);
 pinMode(pin_MEMBRANE_BTN, OUTPUT);
 pinMode(pin_MAG_INT, INPUT);
 pinMode(pin_MAG    , INPUT);

}
void loop() {
 int x;
 x = analogRead (0);
 x = 50;
 lcd.setCursor(10,1);
 if (x < 60) {
   lcd.print ("Right ");

   val = analogRead(pin_MAG);
   lcd.setCursor(10,1);
   lcd.print (val);

   digitalWrite(pin_MAG, LOW);
   digitalWrite(pin_MAG_INT, LOW);
   pinMode(pin_MAG, OUTPUT);
   pinMode(pin_MAG_INT, OUTPUT);

   for(int i=8; i > 0; i--)
   {
      lcd.setCursor(10,1);
      lcd.print ("     ");
      lcd.setCursor(10,1);
      lcd.print (i);
      delay(1000);
   }

   pinMode(pin_MAG, INPUT);
   pinMode(pin_MAG_INT, INPUT);
   val = analogRead(pin_MAG);
   lcd.setCursor(10,1);
   lcd.print (val);
   exit(0);
 }
 else if (x < 200) {
   lcd.print ("Up    ");
//   digitalWrite(53, HIGH);
    analogWrite(pin_MAG_INT, 255); // 5V
//    analogWrite(pin_MEMBRANE_BTN, 63); // 4V
    delay(500);
 }
 else if (x < 400){
    lcd.print ("Down  ");
//    digitalWrite(53, LOW);
//    digitalWrite(pin_MEMBRANE_BTN, HIGH);       // sets the digital pin 13 on
    analogWrite(pin_MAG_INT, 0);
    delay(500);
 }
 else if (x < 600){
   lcd.print ("Left  ");

   val = analogRead(pin_MAG);
   lcd.setCursor(10,1);
   lcd.print (val);

   digitalWrite(pin_MAG, LOW);
   digitalWrite(pin_MAG_INT, LOW);
   pinMode(pin_MAG, OUTPUT);
   pinMode(pin_MAG_INT, OUTPUT);

   for(int i=12; i > 0; i--)
   {
      lcd.setCursor(10,1);
      lcd.print ("     ");
      lcd.setCursor(10,1);
      lcd.print (i);
      delay(1000);
   }

   pinMode(pin_MAG, INPUT);
   pinMode(pin_MAG_INT, INPUT);
   val = analogRead(pin_MAG);
   lcd.setCursor(10,1);
   lcd.print (val);
 }
 else if (x < 800){
   lcd.print ("Select");

   // 3.85V =
   analogWrite(pin_PWR, 128);
 }
}

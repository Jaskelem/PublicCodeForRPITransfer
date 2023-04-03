#include <VirtualWire.h> // This library provides features to send short messages, without addressing, retransmit or acknowledgment

const int yPin = A0;  // analog pin for the x-axis of the left stick
const int xPin = A1;  // analog pin for the y-axis of the left stick
const int inputPin1 = 3;  //button input pins 
const int inputPin2 = 4;  //button input pins
const int inputPin3 = 5;  //button input pins

const int transmitPin = 8; // pin for the transmitter
const int baudRate = 2000; //This baud rate works best for me from my tests

void setup() {
  Serial.begin(9600);
  //Set up transmiter
  vw_set_tx_pin(transmitPin);
  vw_setup(baudRate);
  //Set up button pins
  pinMode(inputPin1,INPUT);
  pinMode(inputPin2,INPUT);
  pinMode(inputPin3,INPUT);
}

void loop() {
  //Set sent to 0 , this makes that if there was an input error it will send a signal with 0
  int send = 0;
  //Read digital button pins
  int push1=digitalRead(inputPin1);
  int push2=digitalRead(inputPin2);
  int push3=digitalRead(inputPin3);

  int xValue = analogRead(xPin);  // read the value of the x-axis from joistick
  int yValue = analogRead(yPin);  // read the value of the y-axis from joistick

  // print the values to the serial monitor
  Serial.print("X: ");
  Serial.print(xValue);
    Serial.print(" Y: ");
  Serial.println(yValue);
  //Encodes Each input with a diffrent code ,so the receiver would have an easyer time telling them appart
  send=10000+xValue;
  vw_send((uint8_t*)&send, sizeof(send));
  send=20000+yValue;
  vw_send((uint8_t*)&send, sizeof(20000+xValue));
  if (push1==HIGH) {send=30000;vw_send((uint8_t*)&send, sizeof(send));Serial.print("Button1\n");}
  if (push2==HIGH) {send=40000;vw_send((uint8_t*)&send, sizeof(send));Serial.print("Button2\n");}
  if (push3==HIGH) {send=50000;vw_send((uint8_t*)&send, sizeof(send));Serial.print("Button3\n");}

 //Sets buttons to low just in case
  push1=LOW;
  push2=LOW;
  push3=LOW;

  delay(100);  // wait for 100 milliseconds
}

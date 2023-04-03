#!/usr/bin/env python

import time
import os     #importing os library so as to communicate with the system
os.system ("sudo pigpio-master/pigpiod") #Launching GPIO library
time.sleep(1) # Needs delay or an error will happen

import pigpio #pigpio is a library for the Raspberry which allows control of the General Purpose Input Outputs (GPIO)
import piVirtualWire_master.piVirtualWire as vw #piVirtualWire is an arduino virtualWire library for python

RX_PIN = 17 #pin for the receiver
BAUD_RATE = 2000 #the rate at which information is transferred in a communication channel

# Initiate libraries
pi = pigpio.pi()
rx = vw.rx(pi, RX_PIN, BAUD_RATE)

#Reads the incomming radio signal and converts it from bytes to number
def RadioSignal():
    while rx.ready():
        message_bytes = rx.get()
        message=int.from_bytes(message_bytes[:2], byteorder='little')
        return message




if __name__ == "__main__":
    while True:
        signal=RadioSignal()
        print(signal)
       # if(signal != None):
            #if(round(signal / 10000) >2):
             #   print("----------------------------------------")
              #  print(signal)
             #   print("----------------------------------------")
        #print(signal)
        time.sleep(0.08)

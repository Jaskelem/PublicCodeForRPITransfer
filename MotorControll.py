"""
A2212 1000 kV Brushless Outrunner Motor Controll Code
These motors are not well suited for programing and require extra
management to make them work.

Flight direction based on frame colors
Black forward
White Back
"""
import time
import os     #importing os library so as to communicate with the system
os.system ("sudo pigpio-master/pigpiod") #Launching GPIO library
time.sleep(1) # Needs delay or an error will happen
import pigpio #importing GPIO library


motor1=23  #Connect the ESC in this GPIO pin
motor2=27  #Connect the ESC in this GPIO pin
motor3=22  #Connect the ESC in this GPIO pin
motor4=10  #Connect the ESC in this GPIO pin

#1st motor left black
#2st motor right black
#3st motor left white
#4st motor right white
#rearange this depending on how motors are wired
motors=[motor1,motor2,motor3,motor4]

pi = pigpio.pi();

maxValue = 2400 #This is the maximum frequancy that i chose for the motors
minValue = 1500  #This is the minimum frequancy that i chose for the motors, it doesnt beep in this frequancy but it doesnt move either, only starts rotating at about 1518
currentState1=minValue
currentState2=minValue
currentState3=minValue
currentState4=minValue

#This step is required for priming the ESC,without this section the motor will not rotate on command
def StartUp():
    for power in range(minValue,1518,1):
        for motor in motors:
            pi.set_servo_pulsewidth(motor, power)
        time.sleep(0.01)
    #Stop()

#Reduces motor speed to minimum and stops GPIO from working
def Stop():
    for motor in motors:
        pi.set_servo_pulsewidth(motor, minValue)
    pi.stop()

#Tests motors
def Test():
    for power in range(1517,1550,1):
        for motor in motors:
            pi.set_servo_pulsewidth(motor, power)
        print(power)
        time.sleep(5)
    Stop()

#Changes motor speed based on inputs
#motor - Select which motor to change speed
#CurrentState - The current speed of motor
#power - the number that will alter the current speed,can be a negative for reduction
def ChangeSpeed(motor,currentState,power):
    currentState=currentState+power
    print("Power: "+str(power))
    
    #A precaution to protect the motors from being set to the wrong frequincy
    if (currentState<minValue):
        currentState=minValue
        pi.set_servo_pulsewidth(motor, currentState)
    elif (currentState>maxValue):
        currentState=maxValue
        pi.set_servo_pulsewidth(motor, currentState)
    else:
        pi.set_servo_pulsewidth(motor, currentState)
    
    print("CurrentState: "+str(currentState)+" Motor: "+str(motor))
    return currentState

#Saves the current motor settings and updates them based on the power parameter provided
def MotorSpeed(motor,power):
    global currentState1
    global currentState2
    global currentState3
    global currentState4
    
    if(motor==motors[0]):
        currentState1=ChangeSpeed(motor,currentState1,power)
    elif(motor==motors[1]):
        currentState2=ChangeSpeed(motor,currentState2,power)
    elif(motor==motors[2]):
        currentState3=ChangeSpeed(motor,currentState3,power)
    elif(motor==motors[3]):
        currentState4=ChangeSpeed(motor,currentState4,power)
    else:
        print("Bad Parameters in Motor Speed")

if __name__ == "__main__":
    StartUp()
    print("done")
    print(currentState1)
    for i in range(0,200,1):
        for motor in motors:
            MotorSpeed(motor,1)
        time.sleep(0.01)
    print("motor speed set")
    time.sleep(5)
    Stop()
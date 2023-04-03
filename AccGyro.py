'''
        Read Gyro and Accelerometer by Interfacing Raspberry Pi with MPU6050 using Python
    http://www.electronicwings.com

    Black moves forward
    White moves back
    -Gy tilt forward
    +Gy tilt back
    +Gx tilt left
    -Gx tilt right
    Gz rotate
    +Ax moves forward
    -Ax moves backward
    Az moves up or down
'''
import smbus            #import SMBus module of I2C
from time import sleep   
import math             #import math for some floor rounding

bus = smbus.SMBus(1)    # or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address (Accelerometer/Gyroscope)

#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47

def MPU_Init():
    
    #write to sample rate register
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)

    #Write to power management register
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)

    #Write to Configuration register
    bus.write_byte_data(Device_Address, CONFIG, 0)

    #Write to Gyro configuration register
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)

    #Write to interrupt enable register
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)


def read_raw_data(addr):
    #Accelero and Gyro value are 16-bit
        high = bus.read_byte_data(Device_Address, addr)
        low = bus.read_byte_data(Device_Address, addr+1)
    
        #concatenate higher and lower value
        value = ((high << 8) | low)
        
        #to get signed value from mpu6050
        if(value > 32768):
                value = value - 65536
        return value

def GyroscopeInfo():
    #Read Gyroscope raw value
    gyro_x = read_raw_data(GYRO_XOUT_H)
    gyro_y = read_raw_data(GYRO_YOUT_H)
    gyro_z = read_raw_data(GYRO_ZOUT_H)

    #adjust data so it would be more accurate and usefull
    Gx = round(gyro_x/131.0,2)
    Gy = round(gyro_y/131.0,2)
    Gz = round(gyro_z/131.0,2)

    Gx=Gx+0.12
    Gy=Gy-0.23
    #Gz=Gz+0.005

    return Gx,Gy,Gz

def AccelerometerInfo():
    #Read Accelerometer raw value
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_YOUT_H)
    acc_z = read_raw_data(ACCEL_ZOUT_H)

    #adjust data so it would be more accurate and usefull
    Ax = round(acc_x/16384.0,3)
    Ay = round(acc_y/16384.0,3)
    Az = round(acc_z/16384.0,3)

    Ax=Ax+0.06
    Ay=Ay+0.03
    Az=Az-0.9999

    return Ax,Ay,Az

#Average out the info in five reads, helps eliminate a lot of noise
def AverageInfo():
    
    TGx=0
    TGy=0
    TGz=0
    TAx=0
    TAy=0
    TAz=0
    for i in range(0,5,1):
        Gx,Gy,Gz=GyroscopeInfo()
        Ax,Ay,Az=AccelerometerInfo()
        TGx=+Gx
        TGy=+Gy
        TGz=+Gz
        TAx=+Ax
        TAy=+Ay
        TAz=+Az
    TGx=round(math.floor(TGx/5*1000)/1000,1)
    TGy=round(math.floor(TGy/5*1000)/1000,1)
    TGz=round(math.floor(TGz/5*1000)/1000,1)
    TAx=round(math.floor(TAx/5*1000)/1000,2)
    TAy=round(math.floor(TAy/5*1000)/1000,2)
    TAz=round(math.floor(TAz/5*1000)/1000,2)
    return TGx,TGy,TGz,TAx,TAy,TAz

#used for testing, prints only if there are changes in the reading      
def DifferentAllResult():
    Gx,Gy,Gz,Ax,Ay,Az=AverageInfo()
    if (Gx != 0 or Gy != 0 or Gz != 0 or Ax != 0 or Ay != 0 or Az != 0):
        print ("Gx=%s" %Gx, u'\u00b0'+ "/s", "\tGy=%s" %Gy, u'\u00b0'+ "/s", "\tGz=%s" %Gz, u'\u00b0'+ "/s", "\tAx=%s g" %Ax, "\tAy=%s g" %Ay, "\tAz=%s g" %Az)
    



if __name__ == "__main__":
    
    MPU_Init()
    print (" Reading Data of Gyroscope and Accelerometer")
    while True:
        DifferentAllResult()
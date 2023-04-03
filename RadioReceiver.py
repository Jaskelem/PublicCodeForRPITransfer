#!/usr/bin/env python
#Old code for Radio receiver that didint work consistently
import argparse
import signal
import sys
import time
import logging

from rpi_rf import RFDevice

rfdevice = None

# pylint: disable=unused-argument
def exithandler(signal, frame):
    rfdevice.cleanup()
    sys.exit(0)

logging.basicConfig(level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',
                    format='%(asctime)-15s - [%(levelname)s] %(module)s: %(message)s', )

parser = argparse.ArgumentParser(description='Receives a decimal code via a 433/315MHz GPIO device')
parser.add_argument('-g', dest='gpio', type=int, default=17,
                    help="GPIO pin (Default: 27)")
args = parser.parse_args()

signal.signal(signal.SIGINT, exithandler)
rfdevice = RFDevice(args.gpio)
rfdevice.enable_rx()
timestamp = None
logging.info("Listening for codes on GPIO " + str(args.gpio))
while True:
    if rfdevice.rx_code_timestamp != timestamp:
        timestamp = rfdevice.rx_code_timestamp
        if round(rfdevice.rx_code / 10000) == 1:
            logging.info("X: "+ str(rfdevice.rx_code % 10000))
        if round(rfdevice.rx_code / 10000) == 2:
            logging.info("Y: "+ str(rfdevice.rx_code % 10000))
        if round(rfdevice.rx_code / 10000) == 3:
            logging.info("1: "+ str(rfdevice.rx_code % 10000))
        if round(rfdevice.rx_code / 10000) == 4:
            logging.info("2: "+ str(rfdevice.rx_code % 10000))
        if round(rfdevice.rx_code / 10000) == 5:
            logging.info("3: "+ str(rfdevice.rx_code % 10000))
                     
    time.sleep(0.1)
rfdevice.cleanup()
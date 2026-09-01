import serial.tools.list_ports
import time
import os
import utils as utilities
import argparse
from datetime import datetime
import psutil
import csv
import math
import os
import shutil

print("Monitoring Disabling Command 1")
if not  utilities.waitPartUart(MCU_COM,"if ! grep -q '^python3 /git/git/app/main\\.py.*--no-monitoring' /git/git/app/run.sh; then", 10, expected='>') : exit(1) 
time.sleep(1)  

print("Monitoring Disabling Command 2")
if not  utilities.waitPartUart(MCU_COM,"echo 'Appending --no-monitoring to python3 line in /git/git/app/run.sh'", 10, expected='>') : exit(1) 
time.sleep(1)  

print("Monitoring Disabling Command 3")
if not  utilities.waitPartUart(MCU_COM,"sed -i '/^python3 /git/git/app/\\/main\\.py/ s|$| --no-monitoring|' /git/git/app/run.sh", 10, expected='>') : exit(1) 
time.sleep(1)  

print("Monitoring Disabling Command 4")
if not  utilities.waitPartUart(MCU_COM,"else", 10, expected='>') : exit(1) 
time.sleep(1)  

print("Monitoring Disabling Command 5")
if not  utilities.waitPartUart(MCU_COM,"echo '--no-monitoring already present, skipping.'", 10, expected='>') : exit(1) 
time.sleep(1)  

print("Monitoring Disabling Command 6")
if not  utilities.waitPartUart(MCU_COM,"fi", 10, expected='--no-monitoring') : exit(1) 
time.sleep(5)  

print("Monitoring Disabling Command 7")
if not utilities.waitPartUart(MCU_COM,"exit", 120, expected='AVIVA bootup time') : 
    if not utilities.waitPartUart(MCU_COM,"exit", 120, expected='AVIVA bootup time') :exit(1) 
time.sleep(1)  

print("Monitoring Disabling Command 8")
utilities.waitFromtUart(MCU_COM, 60, expected='SELECT>')  
time.sleep(1)  

print("Monitoring Disabling Command 9")
if not  utilities.waitPartUart(MCU_COM,"\n", 10, expected='SELECT>') : exit(1) 
time.sleep(1) 

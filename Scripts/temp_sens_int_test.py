import subprocess

# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Test interrupt line for tempratur sensor 
# Parameters:
# $1 - Bus number
# $2 - Device number
# Return: None
# =-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
def check_temp_int(bus, dev):
    cur_temp   = 0
    org_t_low  = 0
    org_t_high = 0
    cur_t_low  = 0
    cur_t_high = 0

    print ("*****************************************")
    print (f"* Testing Temp Dev {dev}, on i2c bus {bus}")
    print ("*****************************************")

    # --->>> Set Configuration Reg (0x01).:
    #  - OS  =  '1': Set 'One-Shot' mode 
    #  - FQ  = '00': Trigger ALERT adter 1 fault (defult)
    #  - POL =  '0': ALERT active Low (default)
    #  - TM  =  '1': ALERT in interrupt mode
    #  - SD  =  '0': Clear 'Shutdown Mode' 
    #  0010 0010 = 0x22
    subprocess.run(["i2cset", "-y", "-f", bus, dev, "0x01", "0x22"])
    
    # --->>> Write 'One-Shot' register to start conversion (Addr=0x04)
    subprocess.run(["i2cset", "-y", "-f", bus, dev, "0x04", "0x00"])
    
    # --->>> Read current temperature from device (Addr=0x00)
    cur_temp = subprocess.run(["i2cget", "-y", "-f", bus, dev, "0x00", "w"], capture_output=True, text=True)
    print (f"Current Temp: {cur_temp.stdout.strip()}")
    
    # --->>> Read original values of T-Low/T-High for restoration after test
    org_t_low = subprocess.run(["i2cget", "-y", "-f", bus, dev, "0x02", "w"], capture_output=True, text=True)
    org_t_high = subprocess.run(["i2cget", "-y", "-f", bus, dev, "0x03", "w"], capture_output=True, text=True)
    
    # --->>> Set T-Low Temp limit (Addr 0x02) to 1c
    subprocess.run(["i2cset", "-y", "-f", bus, dev, "0x02", "0x0001", "w"])
    
    # --->>> Set T-High Temp limit (Addr 0x03) to 5c
    subprocess.run(["i2cset", "-y", "-f", bus, dev, "0x03", "0x0005", "w"])
    
    # --->>> Write 'One-Shot' register to start conversion (Addr=0x04)
    subprocess.run(["i2cset", "-y", "-f", bus, dev, "0x04", "0x00"])
     
    # --->>> Re-read values of T-Low/T-High
    cur_t_low  = subprocess.run(["i2cget", "-y", "-f", bus, dev, "0x02", "w"], capture_output=True, text=True)
    cur_t_high = subprocess.run(["i2cget", "-y", "-f", bus, dev, "0x03", "w"], capture_output=True, text=True)
    print (f"Current T-Low: {cur_t_low}, T-High: {cur_t_high}")
    
    # --->>> TODO: Read GPIO to see if interrupt is activated
    
    # --->>> Restore original values of T-Low/T-High before moving to next device
    print (f"Restoring Org T-Low: {org_t_low} T-High: {org_t_high}")
    subprocess.run(["i2cset", "-y", "-f", bus, dev, "0x02", org_t_low, "w"])
    subprocess.run(["i2cset", "-y", "-f", bus, dev, "0x03", org_t_high, "w"])
    
# ---->>>> Call tests for all devices...
check_temp_int("0x04", "0x48")

    
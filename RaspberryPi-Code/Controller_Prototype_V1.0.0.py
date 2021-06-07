#    This is my prototype of the code required to control the arduino from the raspberry Pi. This code is a fully working
#    simulation of real code. This code works and I have checked the IR component of the Arduino to make sure that it is
#    recieving the correct code and transmitting it.
#    NOTE!!!! this code can only be run on a raspberry Pi as it makes use of its serial and USB ports
#=====================================================================
#                      SetUp                                 |Working|
#=====================================================================
USB_PORT = "/dev/ttyACM0" # Arduino Uno connection
import urllib.request,json
import serial
import time

#=====================================================================
#                      ThingSpeak Keys                       |Working|
#=====================================================================
READ_API_KEY= '9LNTPOF0OOLKGE7K'
CHANNEL_ID= 1375220

#=====================================================================
#                      Global Variables                      |Working|
#=====================================================================
i = 0 #misc
SEQ = 0 #this will be used to make sure that a certain sequence is not run repeastedly and that it is only run if the even order has changed
Temp = 0
SEQ2 = 0
count = 0 #keeps track of the number of cycles the program has run 
check = 0 # this is used to check to make sure that a real temperature value is recieved from the Particle Argon
#status = "Unknown" # shows status of site collecting data
StartUp = 0 # this is to check of the startUp sequence has been run yet
Dyson_Fan = 1
Dyson_Temp = 22
Dyson_Power = "Off"
Time_of_Day = "TBD"
Power_State = "Off"
Dyson_Cool_Mode = "Off"
Dyson_Night_Mode = "Off"

#=====================================================================
#                      Functions                             |Working|
#=====================================================================

def Retrieve_Particle():
    conn = urllib.request.urlopen("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s" \
                           % (CHANNEL_ID,READ_API_KEY))

    response = conn.read()
    global status
    status = (print("http status code=%s" % (conn.getcode())))
    data=json.loads(response)
    global Temp
    Temp = float((data['field1']))
    #print(Temp)
    conn.close()
#=====================================================================
#               Connect and Test Serial Port                 |Working|
#=====================================================================
# Connect to USB serial port at 9600 baud
try:
   usb = serial.Serial(USB_PORT, 9600, timeout=2)
except:
   print("ERROR - Could not open USB serial port.  Please check your port name and permissions.")
   print("Exiting program.")
   exit()    
#=====================================================================
#   Main Code Infinte Loop | Sends instructions to Arduino   |Working|
#=====================================================================

while True:
    #=====================================================================
    #                      Start Up Sequence
    #=====================================================================
    if StartUp == 0:
        print("============================Starting System V1.0============================")
        print("=================Connection To USB Serial Port Successful✓==================")
        StartUp = 1
    
    time.sleep(6)
    #while 1 > i: # check runs first time regardless
    #    global temp
    #    Retrieve_Particle()
    #    check = Temp
    #    print(i,"Current value")
    #    if check > 5.0: # If temp value is acceptable(real) use that value otherwise keep testing recieved temp values
    #        print(status)
    #        print(Temp)
    #        i = 10
    #        print(i,"Update value")
    Retrieve_Particle()
    print(Temp)
            
#=====================================================================
#                      SEQ 1                                 |Working|
#=====================================================================
    if Temp >= 23.0 and Temp <= 23.9 and SEQ != 1:
        print("Temperature acceptable:")
        while Dyson_Temp > 22:
            print("KEY_TempDown")
            usb.write(b'KEY_TempDown')  # send command to Arduino
            Dyson_Temp -= 1
            time.sleep(1)
            SEQ = 1
        while Dyson_Temp < 23:
            print("KEY_TempUp")
            usb.write(b'KEY_TempUp')  # send command to Arduino
            Dyson_Temp += 1 
            time.sleep(1)
            SEQ = 1
        if Dyson_Power == "On":
            time.sleep(.5)
            print("Dyson Signal Off")
            usb.write(b'KEY_Power')  # send command to Arduino
            Dyson_Power = "Off"
            SEQ = 1
#=====================================================================
#                      SEQ 2                                 |Working|
#=====================================================================
    if Temp >= 30.0 and SEQ != 2:
        print("Signal Cooling Mode:")
        usb.write(b'KEY_Cool_Mode')  # send command to Arduino
        Dyson_Cooler_Mode = "On"
        SEQ = 2
#=====================================================================
#                      SEQ 3                                 |Working|
#=====================================================================
    if Temp >= 24.0 and SEQ != 3:
        if Dyson_Cool_Mode == "On":
            time.sleep(.5)
            print("KEY_TempUp")# this cancels cool mode without rasising the temperature KEY_TempDown can also be used as well
            print("Cool Mode Off")
            usb.write(b'KEY_TempUp')  # send command to Arduino
            Dyson_Cool_Mode = "Off"
            SEQ = 3
        if Power_State == "On":
            time.sleep(.5)
            print("KEY_Power")
            Power_State = "Off"
            usb.write(b'KEY_Power')  # send command to Arduino
            print("Dyson Turned Off")
            SEQ = 3        
#=====================================================================
#                      SEQ 4                                 |Working|
#=====================================================================
    if Temp <= 16.0 and SEQ != 4:
        if Power_State == "Off":
            time.sleep(.5)
            print("KEY_Power")
            Power_State = "On"
            usb.write(b'KEY_Power')  # send command to Arduino
            print("Dyson Turned On")
        while Dyson_Temp <= 30.0:
            print("KEY_TempUp")
            usb.write(b'KEY_TempUp')  # send command to Arduino
            Dyson_Temp += 1
            time.sleep(1)
            SEQ = 4
        while Dyson_Fan <= 10:
            print("KEY_FanUp")
            usb.write(b'KEY_FanUp')  # send command to Arduino
            Dyson_Fan += 1
            time.sleep(1)
            SEQ = 4
#=====================================================================
#                      SEQ 5                                 |Working|
#=====================================================================
    if Temp < 23.0 and SEQ != 5:
        if Power_State == "Off":
            time.sleep(.5)
            print("KEY_Power")
            Power_State = "On"
            usb.write(b'KEY_Power')  # send command to Arduino
            print("Dyson Turned On")
        while Dyson_Temp < 28.0:
            print("KEY_TempUp")
            usb.write(b'KEY_TempUp')  # send command to Arduino
            Dyson_Temp += 1
            time.sleep(1)
            SEQ = 5
        while Dyson_Temp > 27.0:
            print("KEY_TempDown")
            usb.write(b'KEY_TempDown')  # send command to Arduino
            Dyson_Temp -= 1
            time.sleep(1)
            SEQ = 5
        while Dyson_Fan >= 3:
            print("KEY_FanDown")
            usb.write(b'KEY_FanDown')  # send command to Arduino
            Dyson_Fan -= 1
            time.sleep(1)
            SEQ = 5
#=====================================================================
#                      SEQ 6                                 |Working|
#=====================================================================
    if Time_of_Day == "Night" and Dyson_Night_Mode != "On":
        Dyson_Night_Mode = "On"
        usb.write(b'KEY_Night_Mode')  # send command to Arduino
        print("KEY_NightMode")
        SEQ = 6
    if Time_of_Day == "Day" and Dyson_Night_Mode != "Off":
        Dyson_Night_Mode = "Off"
        usb.write(b'KEY_Night_Mode')  # send command to Arduino
        print("KEY_Night_Mode")
        SEQ = 6
#=====================================================================
#                      End Debug                             |Working|
#=====================================================================    
    if SEQ2 == SEQ:
        print("Avoiding Repeat Code")
    SEQ2 = SEQ
    #print(SEQ,SEQ2)
    count += 1 
    print("Iteration:",count)
    
    

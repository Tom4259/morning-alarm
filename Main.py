from meross_iot.manager import MerossManager
from meross_iot.cloud.devices.power_plugs import GenericPlug
import alsaaudio
import RPi.GPIO as GPIO
import random
import time
import os
import glob
import sys
from mfrc522 import SimpleMFRC522
import threading

GPIO.setwarnings(False)


def END_PROGRAM():
    print("Program ending...")
    
    alsaaudio.Mixer('PCM').setvolume(70)
    
    GPIO.cleanup()
    sys.exit()


#class alarm:
def RFID_alarm(schoolOut):

    GPIO.setmode(GPIO.BCM)
    
    if schoolOut is True:
        
        #os.system("sudo reboot")
        GPIO.setmode(GPIO.BCM)
        FAN = 5
        GPIO.setup(FAN, GPIO.OUT)
        GPIO.output(FAN, 1)
        
        END_PROGRAM()
        
    RED = 17
    GREEN = 18
    BLUE = 27
    FAN = 5

    GPIO.setwarnings(False)

    sys.path.append('/home/pi/MFRC522-python')

    sys.path.append('/home/pi/lcd/')

    import lcddriver

    reader = SimpleMFRC522()

    display = lcddriver.lcd()

    display.lcd_clear()

    alarm_file = "/tmp/alarm"

    m = alsaaudio.Mixer('PCM')

    #print("Hold a tag near the reader")
    
    


    def check_tag(display):
        display.lcd_clear()
        
        GPIO.setup(BLUE,GPIO.OUT)
        GPIO.output(BLUE,0)
            
        display.lcd_display_string("Checking tag.", 1)
        time.sleep(0.75)
        display.lcd_display_string("Checking tag..", 1)
        time.sleep(0.75)
        display.lcd_display_string("Checking tag...", 1)
        time.sleep(0.75)
        GPIO.output(BLUE,1)
        
        
        display.lcd_clear()

        
    def check_card():
        
        
        display.lcd_clear()
        
        time.sleep(1)
            
        display.lcd_display_string("  Swipe tag to", 1)
        display.lcd_display_string(" disable alarm!", 2)
           
        id, text = reader.read()
        
        print("Checking tag...")
        
        
        if id == <YOUR RFID CHIP PIN>:
            
            
            
            check_tag(display)
            
            print(id)
            print(text)
            
            display.lcd_display_string(" RFID approved!", 1)
            
            display.lcd_display_string(" alarm disabled", 2)
                          
            GPIO.setup(GREEN,GPIO.OUT)
            GPIO.output(GREEN,0)
            time.sleep(0.25)
            GPIO.output(GREEN,1)
            time.sleep(0.25)
            
            GPIO.output(GREEN,0)
            time.sleep(0.25)
            GPIO.output(GREEN,1)
            time.sleep(0.25)
            
            if os.path.exists(alarm_file):
                os.remove(alarm_file)
            
            time.sleep(3)
            
            display.lcd_clear()
            
            END_PROGRAM()
            
        else:
            
            #m.setvolume(62)
                    
            check_tag(display)
            
            print(id)
            print(text)
                   
            display.lcd_display_string("  RFID denied!", 1)
            display.lcd_display_string("  alarm ACTIVE", 2)
            
            GPIO.setup(RED,GPIO.OUT)
            GPIO.output(RED,0)
            time.sleep(2)
            GPIO.output(RED,1)
            
            time.sleep(1)
            
            display.lcd_clear()
            
            check_card()
            

    

    try:
        check_card()
                

    finally:
        END_PROGRAM()

def LIGHT_alarm(schoolOut):

    if schoolOut is True:
        END_PROGRAM()
        
    sys.path.append('/home/pi/lcd/')
    import lcddriver
    #init the lcd display
    DISPLAY = lcddriver.lcd()
                                                                
    ALARM_FILE = "/tmp/alarm"
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)

    #morningText = "/home/pi/Documents/PyMusic/"

    BUZZER_PIN = 21
    GPIO.setup(BUZZER_PIN, GPIO.OUT)

    EMAIL = os.environ.get('MEROSS_EMAIL') or "<MEROSS EMAIL>"
    PASSWORD = os.environ.get('MEROSS_PASSWORD') or "<MEROSS PASSWORD>"

    READING_LIGHT = "Reading Light"
    SONG_DIRECTORY = "/home/pi/Documents/PyMusic/"

    filterRes = glob.glob
    DISPLAY.lcd_clear()
    def displayText(display, text = '', num_line = 1, num_cols = 16):
        """
        Parameters: (driver, string to print, number of line to print, number of columns of your display)
        Return: This function send to display your scrolling string.
        """
        
        if(len(text) > num_cols):
            display.lcd_display_string(text[:num_cols],num_line)
            time.sleep(1.5)
            for i in range(len(text) - num_cols + 1):
                text_to_print = text[i:i+num_cols]
                display.lcd_display_string(text_to_print,num_line)
                time.sleep(0.75)
            time.sleep(1)
        else:
            display.lcd_display_string(text,num_line)


    #alternates between turning the lights on and off and sounding the buzzer
    def soundAlarm(plug):
        plug.turn_on_channel(0)
        GPIO.output(BUZZER_PIN, False)
        
        time.sleep(1)
        
        plug.turn_off_channel(0)
        GPIO.output(BUZZER_PIN, True)
        
        time.sleep(1)    

    #alternates between turning the lights on and off and sounding the buzzer
    def stopAlarm(plug):
        plug.turn_on_channel(0)           
        GPIO.output(BUZZER_PIN, False)
        
    #finds the named plug from the meross manager, else throws an error if missing
    def findPlug(manager,name):
        plugs = manager.get_devices_by_kind(GenericPlug)    #gets the meross device setup(plug)
        
        for plug in plugs:
            if plug.name == name:
                return plug
        
        raise "no plug available"

    def playRandomSong():
        #picks random song
        song = random.choice(findSongs())
        
        #play the mp3 file
        os.system("mpg123 " + song + " &")    
        time.sleep(1)
        
        lines = open('<TEXT FILE>').read().splitlines()
        finalText = random.choice(lines)
        print(finalText)
        
        time.sleep(3)
        
        showMorningText()
        displayText(DISPLAY, finalText, 2)
        
        time.sleep(300)
        
        DISPLAY.lcd_clear()
        
        END_PROGRAM()

    #finds available sounds in the song directory, returns full path name including directory and file
    def findSongs():
        return filterRes(SONG_DIRECTORY + "*.mp3")

    def showMorningText():
        displayText(DISPLAY, "Good morning <YOUR NAME>", 1)
        return


    def setUp():
        
        display = lcddriver.lcd()
        
        display.lcd_clear()
        
        if not os.path.exists(ALARM_FILE):
            open(ALARM_FILE,"a").close()

        alsaaudio.Mixer('PCM').setvolume(70)
        
        GPIO.setmode(GPIO.BCM)
        

    #housekeeping
    setUp()

    # Initiates the Meross Cloud Manager. This is in charge of handling the communication with the remote endpoint
    manager = MerossManager(meross_email=EMAIL, meross_password=PASSWORD)
    # Starts the manager
    manager.start()
    #find the reading light plug, next to the bed
    plug = findPlug(manager, READING_LIGHT)                   
           
    #if the alarm trigger file exists, then we want to make a commotion
    while os.path.exists(ALARM_FILE):        
        soundAlarm(plug)
            
    # the alarm file no longer exists, as it has been turned removed through
    # rfid.alarmTurnOff code               
    stopAlarm(plug)

    #play a random song from the filesystem
    playRandomSong()

    #nice morning message
    showMorningText()
    
    
    
print("Program starting...")
t1 = threading.Thread(target=RFID_alarm, args=(True,), daemon=False)
t2 = threading.Thread(target=LIGHT_alarm, args=(True,), daemon=False)

t1.start()
#print("second thread running")
t2.start()
    

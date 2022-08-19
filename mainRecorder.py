import io, signal, os, sys, traceback, subprocess, threading
import datetime as dt
import RPi.GPIO as GPIO
from time import sleep
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
import random
import digitalio
from pad4pi import rpi_gpio

######################################################################
# DEFINING THE FILE PATHS THAT WILL BE NEEDED THROUGHOUT THIS SCRIPT #
######################################################################
pickupSound = '/home/pizero/recorder/pickupSound/' # file 
buttonTwo = '/home/pizero/recorder/button2/'
buttonThree = '/home/pizero/recorder/button3/'
buttonFour = '/home/pizero/recorder/button4/'
buttonFive = '/home/pizero/recorder/button5/'
buttonSix = '/home/pizero/recorder/button6/'
buttonSeven = '/home/pizero/recorder/button7/'
buttonEight = '/home/pizero/recorder/button8/'
buttonNine = '/home/pizero/recorder/button9/'
dialtone = "/home/pizero/recorder/audio/dial.wav"
beepSound = "/home/pizero/recorder/audio/beep.wav"
recDir  = "/home/pizero/recorder/recordings"
recdir="rec"
filePrefix="recorded"
source = "/home/pizero/recorder/recordings/"
destination = "/home/pizero/recorder/doneRecording/"

play_sound_proc = None
threadWaiter = threading.Event()
rec_sound_proc = None


######################################################################
# DEFINING THE RASPBERRY PI GPIO PINS THAT WILL BE USED. MAKE SURE   #
# THAT YOUR PINOUT (WHERE YOUR WIRES ARE CONNECTED TO THE RPI)       #
# CORRESPOND TO THE CORRECT NUMBERS BELOW. USE THE 'keypad.py'       #
# SCRIPT TO MAKE SURE IT IS CORRECT.                                 #
######################################################################
hookSwitch = 25 # the pin connected to the hook switch (the one triggered when you pick up or put down the phone.)

# SETTING UP THE KEYPAD. IF THERE IS ONE PART THAT MAY REQUIRE SOME TROUBLESHOOTING,
# IT WILL LIKELY BE THIS ONE.
ROW_PINS = [6, 5, 19, 13] # BCM numbering
COL_PINS = [20, 21, 26] # BCM numbering

keys = ((5, 2, 8), 
        (6, 3, 9), 
        (7, 8, 9), 
        (4, 1, 7))

factory = rpi_gpio.KeypadFactory()

keypad = factory.create_keypad(keypad=keys, row_pins=ROW_PINS, col_pins=COL_PINS)

####################
#    FUNCTIONS     #
####################

# stops a keypad button sound and starts a recording.
def stopSoundRecord():
    stopSound()
    threadWaiter.set()

# function that is called when a keypad button is pressed.
# 'threadWaiter.set()' allows the main while loop to continue
# and start a recording. The 'playSound()' function is defined below
# and takes the parameter of an WAV file path. 'buttonsDir' is the
# parent directory for the buttons folders, the random.choice + 
# os.listdir functions are used to get the name of a single random
# filename from the folder of whichever button is pressed.
def recordKey(key):
    if key == 1:
        threadWaiter.set()
    elif key == 2:
        playSound(buttonTwo + random.choice(os.listdir(buttonTwo)))
        if key == 1: stopSoundRecord()
    elif key == 3:
        playSound(buttonThree + random.choice(os.listdir(buttonThree)))
        if key == 1: stopSoundRecord()
    elif key == 4:
        playSound(buttonFour + random.choice(os.listdir(buttonFour)))
        if key == 1: stopSoundRecord()
    elif key == 5:
        playSound(buttonFour + random.choice(os.listdir(buttonFour)))
        if key == 1: stopSoundRecord()
    elif key == 5:
        playSound(buttonFive + random.choice(os.listdir(buttonFive)))
        if key == 1: stopSoundRecord()
    elif key == 6:
        playSound(buttonSix + random.choice(os.listdir(buttonSix)))
        if key == 1: stopSoundRecord()
    elif key == 7:
        playSound(buttonSeven + random.choice(os.listdir(buttonSeven)))
        if key == 1: stopSoundRecord()
    elif key == 8:
        playSound(buttonEight + random.choice(os.listdir(buttonEight)))
        if key == 1: stopSoundRecord()
    elif key == 9:
        playSound(buttonNine + random.choice(os.listdir(buttonNine)))
        if key == 1: stopSoundRecord()

def checkHook():
    global hookSwitch
    return(GPIO.input(hookSwitch) == GPIO.HIGH)

def checkHookStop():
    global hookSwitch
    return(GPIO.input(hookSwitch) == GPIO.HIGH)
    threadWaiter.set()

def waitForSignal():
    global threadWaiter
    threadWaiter.wait() 
    threadWaiter.clear() # clear it after receiving the wakeup

def getTimestamp():
    return dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def getFileTimestamp():
    return dt.datetime.now().strftime('%Y%m%d-%H%M%S')

# responsible for playing all sounds throughout the script.
def playSound(soundName=None):
    global play_sound_proc

    if play_sound_proc is not None: play_sound_proc.terminate()

    play_sound_proc = subprocess.Popen(["aplay", "--device=plughw:1,0", soundName],stdout=subprocess.PIPE,stderr=subprocess.PIPE)

def soundIsPlaying():
    return(play_sound_proc is not None and play_sound_proc.poll() is None)

def stopSound():
    global play_sound_proc

    if play_sound_proc is not None: play_sound_proc.terminate()

# responsible for starting a recording.
def recordSound(recName):
    global rec_sound_proc, recdir

    if rec_sound_proc is not None: rec_sound_proc.terminate()

    print(getTimestamp() + ' : Recording sound: ' + recName)

    rec_sound_proc = subprocess.Popen(["arecord", "--device=plughw:1,0", "--format", "S16_LE", "--rate", "44100", "-c1", recDir + '/' + recName],
                                      stdout=subprocess.PIPE,stderr=subprocess.PIPE)

def soundIsRecording():
    return(rec_sound_proc is not None and rec_sound_proc.poll() is None)

def stopRecord():
    global rec_sound_proc
    print(getTimestamp() + ' : Recording stopped at ' + getTimestamp())
    if rec_sound_proc is not None: rec_sound_proc.terminate()

# The callback function which, when triggered, will set the 
# threadWaiter and allow the while loop to continue.
def gpioEvent(channel):
    global isOnHook, threadWaiter
    try:
        GPIO.setmode(GPIO.BCM)

        if channel == hookSwitch:
            sleep(0.100)
            isOnHook = checkHook()
            threadWaiter.set()

    except:
        e = sys.exc_info()[0]
        print(getTimestamp() + " - Error in even handling! Will proceed anyway:\n\n%s" % e)
        traceback.print_exc()

###################################################################
# TRY BLOCK WHICH IS WHERE ALL THE RELEVANT FUNCTIONS ARE CALLED  #
# WHEN THEY ARE TRIGGERED BY A GPIO EVENT                         #
###################################################################

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(hookSwitch,  GPIO.IN, GPIO.PUD_UP)
    sleep(1)
    GPIO.add_event_detect(hookSwitch,  GPIO.BOTH,    callback=gpioEvent, bouncetime=300)

    isOnHook = checkHook()

    while True:
        sleep(0.1)

        if isOnHook:
            continue

        waitForSignal()

        playSound(dialtone)

        if isOnHook:
            stopSound()
            continue

        sleep(2)

        playSound(pickupSound + random.choice(os.listdir(pickupSound)))

        while soundIsPlaying() and not isOnHook: sleep(.25)

        if isOnHook:
            stopSound()
            continue

        keypad.registerKeyPressHandler(recordKey) # triggers the keypad function.
        waitForSignal() # passes this waitForSignal() function when button 1 is pressed.

        if isOnHook:
            stopSound()
            continue

        stopSound()
        recordSound(getFileTimestamp() + '.wav')
        fileName = getFileTimestamp() + '.wav'

        while soundIsRecording() and not isOnHook: sleep(.25)

        if isOnHook:
            stopRecord()
            os.rename(source + fileName, destination + fileName)
            continue

except:
    e = sys.exc_info()[0]
    print(getTimestamp() + " : Error in loop! Will proceed anyway:\n\n%s" % e)
    traceback.print_exc()
finally:
    GPIO.cleanup()
    stopSound()
    stopRecord()

#!/usr/bin/python3

import io, signal, os, sys, traceback, subprocess, threading
import datetime as dt
import RPi.GPIO as GPIO
from time import sleep
import dropbox
from dropbox.files import WriteMode
from dropbox.exceptions import ApiError, AuthError
import random

prompts = ['/home/pi/activePrompt/promptOne.wav', '/home/pi/activePrompt/promptTwo.wav', '/home/pi/activePrompt/promptThree.wav', '/home/pi/activePrompt/promptFour.wav']
dialtone = "/home/pi/dial.wav"
beepSound = "/home/pi/beep.wav"
recDir  = "/home/pi/recordings"
recdir="rec"
filePrefix="recorded"
source = "/home/pi/recordings/"
destination = "/home/pi/doneRecording/"

hookSwitch = 26
recordButton = 16
stopButton = 23
playSound = 17

threadWaiter = threading.Event()
play_sound_proc = None
rec_sound_proc = None
recordedClipCount = 0


def handle_sigint(signal, frame):
    global term_prog, threadWaiter
    term_prog = True
    print('SIGINT received. Terminating.')
    threadWaiter.set()

def handle_sigterm(signal, frame):
    global term_prog, threadWaiter
    term_prog = True
    print('SIGTERM received. Terminating.')
    threadWaiter.set()

def handle_sigquit(signal, frame):
    global term_prog, threadWaiter
    term_prog = True
    print('SIGQUIT received. Terminating.')
    threadWaiter.set()

def getTimestamp():
    return dt.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def getFileTimestamp():
    return dt.datetime.now().strftime('%Y%m%d-%H%M%S')

def waitForSignal():
    global threadWaiter
    threadWaiter.wait()
    threadWaiter.clear() # clear it after receiving the wakeup

def checkHook():
    global hookSwitch
    return(GPIO.input(hookSwitch) == GPIO.HIGH)

def checkRecordButton():
    global recordButton
    return(GPIO.input(recordButton) == GPIO.HIGH)

def playSound(soundName=None):
    global play_sound_proc

    if play_sound_proc is not None: play_sound_proc.terminate()

    play_sound_proc = subprocess.Popen(["aplay", "--device=plughw:1,0", soundName],stdout=subprocess.PIPE,stderr=subprocess.PIPE)

def soundIsPlaying():
    return(play_sound_proc is not None and play_sound_proc.poll() is None)

def stopSound():
    global play_sound_proc

    if play_sound_proc is not None: play_sound_proc.terminate()

def recordSound(recName):
    global rec_sound_proc, recdir

    if rec_sound_proc is not None: rec_sound_proc.terminate()

    print(getTimestamp() + ' : Recording sound: ' + recName)
    # current "device" spec for recording doesn't seem needed, perhaps because unambiguous, but specifying anyway:
    rec_sound_proc = subprocess.Popen(["arecord", "--device=plughw:1,0", "--format", "S16_LE", "--rate", "44100", "-c1", recDir + '/' + recName],
                                      stdout=subprocess.PIPE,stderr=subprocess.PIPE)

def soundIsRecording():
    return(rec_sound_proc is not None and rec_sound_proc.poll() is None)

def stopRecord():
    global rec_sound_proc

    if rec_sound_proc is not None: rec_sound_proc.terminate()

def gpioEvent(channel):
    global isOnHook, threadWaiter

    try:
        # doesn't seem like this should be necessary, but occasional error complains that this isn't set and fails
        GPIO.setmode(GPIO.BCM)

        if channel == hookSwitch:
            sleep(0.100)
            isOnHook = checkHook()
            threadWaiter.set()
        # elif channel == recordButton:
        #     sleep(0.100)
        #     recordButtonPressed = checkRecordButton
        #     threadWaiter.set()

    except:
        e = sys.exc_info()[0]
        print(getTimestamp() + " - Error in even handling! Will proceed anyway:\n\n%s" % e)
        traceback.print_exc()
        #playSound(errorSound, block=True)  # note potential thread issues since this is separate from most playSound calls

try:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    # GPIO.setup(recordpin,   GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(hookSwitch,  GPIO.IN, GPIO.PUD_UP)
    GPIO.setup(18,GPIO.OUT)
    # GPIO.setup(phonedownpin,  GPIO.IN, GPIO.PUD_UP)
    # GPIO.setup(powerbuttonpin, GPIO.IN, GPIO.PUD_UP)
    # sleep a second to give pins time to settle?
    sleep(1)
    # despite "bouncetime" still must debounce ourselves, but this at least helps give only one event per semantic edge
    GPIO.add_event_detect(hookSwitch,  GPIO.BOTH,    callback=gpioEvent, bouncetime=300)
    # GPIO.add_event_detect(phonedownpin,  GPIO.BOTH,    callback=gpioEvent, bouncetime=200)
    # for the pulse, set bounce time to only get one event per pulse, and just rising to cut down a bit on it since we only care about one edge, and still debounce ourselves in callback
    # GPIO.add_event_detect(recordpin,   GPIO.FALLING, callback=gpioEvent, bouncetime=20)
    
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

        playSound(random.choice(prompts))

        isOnHook = checkHook()

        if isOnHook:
            stopSound()
            continue

        while soundIsPlaying() and not isOnHook: sleep(.25)

        playSound(beepSound)

        if isOnHook:
            stopSound()
            continue

        sleep(2)
        recordSound(getFileTimestamp() + '.wav')
        fileName = getFileTimestamp() + '.wav'

        GPIO.output(18,GPIO.HIGH)

        while soundIsRecording() and not isOnHook: 
            sleep(.25)

        if isOnHook:
            recordedClipCount += 1
            print(getTimestamp() + ' : Recording stopped at ' + getTimestamp() + ' -- recorded count: ' + str(recordedClipCount))
            stopSound()
            stopRecord()
            GPIO.output(18,GPIO.LOW)
            os.rename(source + fileName, destination + fileName)
            continue

except:
    e = sys.exc_info()[0]
    print(getTimestamp() + " : Error in loop! Will proceed anyway:\n\n%s" % e)
    tb = traceback.format_exc()
    f = open("errorFile.txt", "w")
    f.write(tb)
    f.close()
finally:
    GPIO.cleanup()
    stopSound()
    stopRecord()

print('MagicTelephone is done at ' + getTimestamp())

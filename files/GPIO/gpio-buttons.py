#!/usr/bin/python3
from gpiozero import Button
from signal import pause
from subprocess import check_call

# This script will block any I2S DAC e.g. from Hifiberry, Justboom, ES9023, PCM5102A
# due to the assignment of GPIO 19 and 21 to a buttons

# 2018-10-31
# Added the function on holding volume + - buttons to change the volume in 0.3s interval
#
# 2018-10-15
# this script has the `pull_up=True` for all pins. See the following link for additional info: 
# https://github.com/MiczFlor/RPi-Jukebox-RFID/issues/259#issuecomment-430007446
#
# 2017-12-12
# This script was copied from the following RPi forum post:
# https://forum-raspberrypi.de/forum/thread/13144-projekt-jukebox4kids-jukebox-fuer-kinder/?postID=312257#post312257
# I have not yet had the time to test is, so I placed it in the misc folder.
# If anybody has ideas or tests or experience regarding this solution, please create pull requests or contact me.

def def_shutdown():
    check_call("./scripts/playout_controls.sh -c=shutdown", shell=True)

def def_volU():
    check_call("./scripts/playout_controls.sh -c=volumeup", shell=True)

def def_volD():
    check_call("./scripts/playout_controls.sh -c=volumedown", shell=True)

def def_vol0():
    check_call("./scripts/playout_controls.sh -c=mute", shell=True)

def def_next():
    check_call("./scripts/playout_controls.sh -c=playernext", shell=True)

def def_prev():
    check_call("./scripts/playout_controls.sh -c=playerprev", shell=True)

def def_halt():
    check_call("./scripts/playout_controls.sh -c=playerpause", shell=True)

def def_recordstart():
    check_call("./scripts/playout_controls.sh -c=recordstart", shell=True)

def def_recordstop():
    check_call("./scripts/playout_controls.sh -c=recordstop", shell=True)

def def_recordplaylatest():
    check_call("./scripts/playout_controls.sh -c=recordplaylatest", shell=True)

# adjusted by schlizbäda due to usage of HifiBerry MiniAmp:
#shut = Button(3, hold_time=2)
#vol0 = Button(13,pull_up=True)
#volU = Button(16,pull_up=True,hold_time=0.3,hold_repeat=True)
#volD = Button(19,pull_up=True,hold_time=0.3,hold_repeat=True)
#next = Button(26,pull_up=True)
#prev = Button(20,pull_up=True)
#halt = Button(21,pull_up=True)
###shut = Button(3,hold_time=2) # --> Pin 5 # no longer necessary due to OnOffShim
vol0 = Button(13,pull_up=True) # --> Pin 33
volU = Button(12,pull_up=True,hold_time=0.3,hold_repeat=True) # --> Pin 32
volD = Button(6,pull_up=True,hold_time=0.3,hold_repeat=True) # --> Pin 31
next = Button(7,pull_up=True) # --> Pin 26
prev = Button(8,pull_up=True) # --> Pin 24
halt = Button(5,pull_up=True) # --> Pin 29
#reco = Button(6, pull_up=True) # Choose GPIO to fit your hardware
#play = Button(12,pull_up=True) # Choose GPIO to fit your hardware

###shut.when_held = def_shutdown # no longer necessary due to OnOffShim
vol0.when_pressed = def_vol0
volU.when_pressed = def_volU
#When the Volume Up button was held for more than 0.3 seconds every 0.3 seconds he will call a ra$
volU.when_held = def_volU
volD.when_pressed = def_volD
#When the Volume Down button was held for more than 0.3 seconds every 0.3 seconds he will lower t$
volD.when_held = def_volD
next.when_pressed = def_next
prev.when_pressed = def_prev
halt.when_pressed = def_halt
#reco.when_pressed = def_recordstart
#reco.when_released = def_recordstop
#play.when_pressed = def_recordplaylatest

pause()

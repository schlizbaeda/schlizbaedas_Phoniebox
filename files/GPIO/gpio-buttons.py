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


# added by schlizbäda at Jun 07th 2020: helper class for providing global variables and constants
class cls_seekbuttons(object):
    def __init__(self):
        self.gl_button_seekduration = 0
        self.GL_SEEKSLOW = 4
        self.GL_SEEKFAST = 16




def def_shutdown():
    check_call("./scripts/playout_controls.sh -c=shutdown", shell=True)

def def_volU():
    check_call("./scripts/playout_controls.sh -c=volumeup", shell=True)

def def_volD():
    check_call("./scripts/playout_controls.sh -c=volumedown", shell=True)

def def_vol0():
    check_call("./scripts/playout_controls.sh -c=mute", shell=True)




# added by schlizbäda at Jun 7th 2020 for seeking inside audio tracks (rewind, fast forward)
def def_reset_dur():
    cls_seekbuttons.gl_button_seekduration = 0
    cls_seekbuttons.GL_SEEKSLOW = 4
    cls_seekbuttons.GL_SEEKFAST = 16

def def_fast_forward():
    cls_seekbuttons.gl_button_seekduration += 1
    if cls_seekbuttons.gl_button_seekduration >= cls_seekbuttons.GL_SEEKSLOW:
        if cls_seekbuttons.gl_button_seekduration >= cls_seekbuttons.GL_SEEKFAST:
            seekwidth = 15
        else:
            seekwidth = 5
        check_call(f"./scripts/playout_controls.sh -c=playerseek -v=+{seekwidth}", shell=True)
    #check_call("./scripts/playout_controls.sh -c=playernext", shell=True)

def def_rewind():
    cls_seekbuttons.gl_button_seekduration += 1
    if cls_seekbuttons.gl_button_seekduration >= cls_seekbuttons.GL_SEEKSLOW:
        if cls_seekbuttons.gl_button_seekduration >= cls_seekbuttons.GL_SEEKFAST:
            seekwidth = 15
        else:
            seekwidth = 5
        check_call(f"./scripts/playout_controls.sh -c=playerseek -v=-{seekwidth}", shell=True)

# adjusted by schlizbäda at Jun 7th 2020 for distingishing skip or seek
def def_next():
    if cls_seekbuttons.gl_button_seekduration < cls_seekbuttons.GL_SEEKSLOW:
        check_call("./scripts/playout_controls.sh -c=playernext", shell=True)
    cls_seekbuttons.gl_button_seekduration = 0

def def_prev():
    if cls_seekbuttons.gl_button_seekduration < cls_seekbuttons.GL_SEEKSLOW:
        check_call("./scripts/playout_controls.sh -c=playerprev", shell=True)
    cls_seekbuttons.gl_button_seekduration = 0




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
next = Button(7,pull_up=True,hold_time=0.3,hold_repeat=True) # --> Pin 26
prev = Button(8,pull_up=True,hold_time=0.3,hold_repeat=True) # --> Pin 24
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

# event calls adjusted by schlizbäda at Jun 7th 2020:
next.when_pressed = def_reset_dur # added by schlizbäda at Jun 7th 2020
next.when_held = def_fast_forward # added by schlizbäda at Jun 7th 2020
next.when_released = def_next     # adjusted by schlizbäda at Jun 7th 2020
prev.when_pressed = def_reset_dur # added by schlizbäda at Jun 7th 2020
prev.when_held = def_rewind       # added by schlizbäda at Jun 7th 2020
prev.when_released = def_prev     # adjusted by schlizbäda at Jun 7th 2020

halt.when_pressed = def_halt
#reco.when_pressed = def_recordstart
#reco.when_released = def_recordstop
#play.when_pressed = def_recordplaylatest

pause()

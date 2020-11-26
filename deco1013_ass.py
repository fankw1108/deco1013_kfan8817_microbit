# Write your code here :-)
from microbit import *
import utime
import music

#comment
'''
1. the device will produce sound only if the user leaves the backrest for more than 5s
2. check moving speed to determine whether the user is leaving or going to sit
3. allow to adjust the volume
'''

class Rangefinder:
    def __init__(self, pin):
        '''Setup a rangefinder on the specified pin'''
        self.pin = pin

    def distance_cm(self):
        '''Returns the distance from a rangefinder in cm'''
        self.pin.write_digital(0)
        utime.sleep_us(10000)
        self.pin.write_digital(1)
        utime.sleep_us(10000)
        self.pin.write_digital(0)
        init = utime.ticks_us()
        stop = init
        start = init
        flag = False
        timeout = 100000

        while not self.pin.read_digital():
            if utime.ticks_us() - init > timeout:
                return -1

        start = utime.ticks_us()

        while self.pin.read_digital():
            if utime.ticks_us() - start > timeout:
                return -1

        stop = utime.ticks_us()
        distance = (stop - start) * 343 / 20000
        return distance

rf = Rangefinder(pin1)
# Available notes for the music playing
notes = ['c', 'd', 'e', 'f', 'g', 'a', 'b']
# Status of the user
status = 'not sitting'
# This records the time when the system first detects the user not sitting properly
leaving_start = 0

# The device will keep running automatically
while True:
    # The value of the rotary sensor
    val = pin2.read_analog()
    # The device between the detected object and the ultrasonic sensor
    dist = rf.distance_cm()
    # If the distance is less than 5cm, the user is sitting properly
    if dist < 5:
        status = 'sitting'
    # If the distance is more than 40cm, the user is away from the chair
    elif dist > 40:
        status = 'not sitting'
    # Otherwise, the user is not sitting properly
    else:
        # Case when the system first detects the user leaving the backrest
        if status == 'sitting':
            status = 'leaving'
            # Record the first detection time for later use
            leaving_start = utime.ticks_ms()
        elif status == 'leaving':
            # Update how long the user has not been sitting properly
            leaving_time = utime.ticks_ms() - leaving_start
            # Case when the user is not sitting properly for more than 3 seconds
            if leaving_time  >= 3000:
                # The key depends on the angle of the rotary sensor
                key = int(val/206) + 1
                # The note depends on the distance between the user's back and the device
                note_id = int((dist - 5) / 5)
                # The sound will be produced most frequently after 10s of not sitting properly
                if leaving_time > 10000:
                    duration = '1'
                else:
                    # The longer time the user does not sit properly, the more frequently the sound is produced
                    duration = str((int((11000-leaving_time)/1000)))
                # Construct and play the sound
                sound = notes[note_id] + str(key) + ':' + duration
                music.play(sound, loop=False)
        # Case when the user starts to sit down
        elif status == 'not sitting':
            status = 'sitting'


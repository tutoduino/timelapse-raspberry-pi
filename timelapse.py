#!/usr/bin/python3
import time
import libcamera
import signal
from picamera2 import Picamera2, Preview
# Ctrl-C signal handler to stop the camera before program exit
def handler(signum, frame):
    print("Ctrl-c was pressed, stop camera and exit.")
    picam2.stop()
    exit(1)
# Configure the Ctrl-C signal handler
signal.signal(signal.SIGINT, handler)
# Number of picture to capture
nb_pictures = 5000
# Time to wait between each capture
wait_time = 9
# Configure the camera for high resolution still capture
picam2 = Picamera2()
picam2.configure(picam2.create_still_configuration())
picam2.start()
# Configure daylight white balance, disable automatic exposure and set framerate to 1 img/s
# Give time for default still configuration to settle
time.sleep(1)
picam2.set_controls({"AeEnable": False, "AwbEnable": False, "AwbMode": libcamera.controls.AwbModeEnum.Cloudy.Daylight, "FrameRate": 1.0})
# And wait for those settings to take effect
time.sleep(1)
# Run autofocus cycle
success = picam2.autofocus_cycle(wait=False)
status = picam2.wait(success)
counter = 0
start_time = time.time()
previous_time = start_time
for i in range(0, nb_pictures):
    filename = "image{:05d}.jpg".format(i)
    r = picam2.capture_request()
    r.save("main", filename)
    r.release()
    current_time = time.time()
    print("Capture saved: {} at time {:.1f}".format(filename,current_time-start_time))
    # Check the time between two capture remains acceptable (2*wait_time),
    # otherwise the impact will be visible in the time-lapse video
    if (current_time - previous_time > wait_time *2):
        print("Timing issue !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    previous_time = current_time 
    time.sleep(wait_time)
picam2.stop()

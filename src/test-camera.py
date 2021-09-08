import logging
from time import sleep
from picamera import PiCamera
import os

directory_path = os.getcwd()
img_path = directory_path + '/test/hello1.jpg';
print("My current directory is : " + directory_path)
print('This is a test for the camera module and will capture an image to ' + img_path)

camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()
# Camera warm-up time
sleep(2)
camera.capture(img_path)
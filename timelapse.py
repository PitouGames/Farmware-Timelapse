#!/usr/bin/env python

'''Take a photo with a specific camera.'''

import os
from time import time, sleep
import cv2
from farmware_tools import device, get_config_value, env

def image_filename():
    'Prepare filename with timestamp.'
    return 'timelapse-{timestamp}.jpg'.format(timestamp=int(time()))

def upload_path(filename):
    'Filename with path for uploading an image.'
    images_dir = env.Env().images_dir or '/tmp/images'
    if not os.path.isdir(images_dir):
        device.log('{} directory does not exist.'.format(images_dir), 'error')
    path = images_dir + os.sep + filename
    return path

def usb_camera_photo(camera_port):
    'Take a photo using a USB camera.'
    # Settings
    discard_frames = 20  # number of frames to discard for auto-adjust

    # Check for camera
    if not os.path.exists('/dev/video' + str(camera_port)):
        print('No camera detected at video{}.'.format(camera_port))
        device.log('USB Camera at video{} not detected.'.format(
            camera_port), 'error', ['toast'])

    # Open the camera
    camera = cv2.VideoCapture(camera_port)
    sleep(0.1)

    # Let camera adjust
    for _ in range(discard_frames):
        camera.grab()

    # Take a photo
    ret, image = camera.read()

    # Close the camera
    camera.release()

    # Output
    if ret:  # an image has been returned by the camera
        filename_path = upload_path(image_filename())
        # Save the image to file
        cv2.imwrite(filename_path, image)
        print('Image saved: {}'.format(filename_path))
        device.log('Image saved: {}'.format(filename_path), 'debug')
    else:  # no image has been returned by the camera
        device.log('Problem getting image from video{}.'.format(
            camera_port), 'error', ['toast'])

if __name__ == '__main__':
    #path = '/tmp/images'
    #dir_list = os.listdir(path)
    #device.log('Files and directories in: {}\n{}'.format(path, dir_list), 'debug')

    CAMERA_PORT = get_config_value('Timelapse', 'camera_port')
    device.log('CAMERA_PORT: {}'.format(CAMERA_PORT), 'debug')
    usb_camera_photo(CAMERA_PORT)

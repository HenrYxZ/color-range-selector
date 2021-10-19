'''
Copyright (C) 2014 Hernaldo Jesus Henriquez Nunez

This program is free software; you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
'''

import cv2 as cv
import numpy as np


ESC_KEY = 27
current_img = 0
segmentation_img = 0
# If option_rgb is true the range will be BGR, else it will be HSV
option_rgb = True
img_count = 0
is_rgb = True


def nothing(x):
    pass


def refresh():
    global current_img
    global segmentation_img
    global is_rgb
    global option_rgb

    ch1_min = cv.getTrackbarPos("min_channel1", "Bars")
    ch1_max = cv.getTrackbarPos("max_channel1", "Bars")
    ch2_min = cv.getTrackbarPos("min_channel2", "Bars")
    ch2_max = cv.getTrackbarPos("max_channel2", "Bars")
    ch3_min = cv.getTrackbarPos("min_channel3", "Bars")
    ch3_max = cv.getTrackbarPos("max_channel3", "Bars")

    min_range = np.array([ch1_min, ch2_min, ch3_min])
    max_range = np.array([ch1_max, ch2_max, ch3_max])

    if not option_rgb and is_rgb:
        current_img = cv.cvtColor(current_img, cv.COLOR_BGR2HSV)
        print("changed Image to HSV")
        is_rgb = False
    segmentation_img = cv.inRange(current_img, min_range, max_range)
    cv.imshow("Segmentation", segmentation_img)


def main():
    '''
	runs a window with the camera image, a processed image and the trackbars for
	the inRange
	'''
    global current_img
    global segmentation_img
    global img_count
    global is_rgb
    global option_rgb

    opt = input("Enter [0] to use a video or [1] to use an image\n")

    ################################################################################
    #####################            Using Video               #####################
    ################################################################################

    if opt == 0:
        path = input("Write the path for your video, 0 to use default webcam\n")
        if path == '0':
            path = 0
        video = cv.VideoCapture(path)
        if video is None or not video.isOpened():
            print('Warning: unable to open video source: ' + path)
            return
        input(
            "At runtime you can press [r] to use BGR range,\n" +
            "[h] to use HSV, [esc] to exit, [space] to pause the video\n" +
            "and [s] to save the segmentation image.\n" +
            "Now press [Enter] to continue ...\n"
        )
        # Important windows
        cv.namedWindow("Bars")
        cv.namedWindow("Segmentation")
        cv.namedWindow("Video")
        cv.createTrackbar("min_channel1", "Bars", 0, 254, nothing)
        cv.createTrackbar("max_channel1", "Bars", 255, 255, nothing)
        cv.createTrackbar("min_channel2", "Bars", 0, 254, nothing)
        cv.createTrackbar("max_channel2", "Bars", 255, 255, nothing)
        cv.createTrackbar("min_channel3", "Bars", 0, 254, nothing)
        cv.createTrackbar("max_channel3", "Bars", 255, 255, nothing)
        pause = False
        while True:
            if not pause:
                ret, current_img = video.read()
                if not ret:
                    break
                cv.imshow("Video", current_img)
            is_rgb = True
            refresh()
            key = cv.waitKey(33)
            if key == ord(' '):
                pause = not pause
                print ("Video paused")
            elif key == ord('r'):
                option_rgb = True
                if not is_rgb:
                    current_img = cv.cvtColor(current_img, cv.COLOR_HSV2BGR)
                print ("Now using BGR range")
            elif key == ord('h'):
                option_rgb = False
                print ("Now using HSV range")
            elif key == ord('s'):
                filename = "{0}.jpg".format(img_count)
                cv.imwrite(filename, current_img)
                print ("Image saved as {0}".format(filename))
                img_count = img_count + 1
            elif key == 27:
                break
        video.release()

    ################################################################################
    #####################            Using Image               #####################
    ################################################################################

    else:
        path = input("Enter the image name: ")
        print("your path is " + path)
        current_img = cv.imread(path)
        if not current_img.any():
            print("Image could not be open")
            return
        else:
            h, w, channels = current_img.shape
        # Resize if the image is too big
        if h > 480:
            new_w = int((480 * w) / h)
            print(f"Using new width of {new_w}")
            current_img = cv.resize(current_img, (new_w, 480))
        input(
            "At runtime you can press [r] to use BGR range,\n" +
            "[h] to use HSV, [esc] to exit\n" +
            "and [s] to save the segmentation image.\n" +
            "Now press [Enter] to continue ...\n"
        )
        # Important windows
        cv.namedWindow("Bars")
        cv.namedWindow("Segmentation")
        cv.namedWindow("Image")
        cv.createTrackbar("min_channel1", "Bars", 0, 254, nothing)
        cv.createTrackbar("max_channel1", "Bars", 255, 255, nothing)
        cv.createTrackbar("min_channel2", "Bars", 0, 254, nothing)
        cv.createTrackbar("max_channel2", "Bars", 255, 255, nothing)
        cv.createTrackbar("min_channel3", "Bars", 0, 254, nothing)
        cv.createTrackbar("max_channel3", "Bars", 255, 255, nothing)
        cv.imshow("Image", current_img)
        while True:
            refresh()
            key = cv.waitKey(33)
            if key == ord('r'):
                option_rgb = True
                if not is_rgb:
                    current_img = cv.cvtColor(current_img, cv.COLOR_HSV2BGR)
                    print ("changed Image to BGR")
                    is_rgb = True
            elif key == ord('h'):
                option_rgb = False
                print ("Now using HSV range")
            elif key == ord('s'):
                filename = "{0}.jpg".format(img_count)
                cv.imwrite(filename, segmentation_img)
                print ("Image saved as {0}".format(filename))
                img_count = img_count + 1
            elif key == 27:
                break
    cv.destroyAllWindows()


if __name__ == '__main__':
    main()

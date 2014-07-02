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

import cv2
import numpy as np

current_img = 0
# If option_rgb is true the range will be BGR, else it will be HSV
option_rgb = True

def nothing(x):
	pass

def new_range():

	global current_img

	ch1_min = cv2.getTrackbarPos("min_channel1", "Bars")
	ch1_max = cv2.getTrackbarPos("max_channel1", "Bars")

	ch2_min = cv2.getTrackbarPos("min_channel2", "Bars")
	ch2_max = cv2.getTrackbarPos("max_channel2", "Bars")

	ch3_min = cv2.getTrackbarPos("min_channel3", "Bars")
	ch3_max = cv2.getTrackbarPos("max_channel3", "Bars")

	min_range = np.array([ch1_min, ch2_min, ch3_min])
	max_range = np.array([ch1_max, ch2_max, ch3_max])

	if not option_rgb:
		img = cv2.cvtColor(current_img, cv2.COLOR_BGR2HSV)
	img = cv2.inRange(current_img, min_range, max_range)
	cv2.imshow("Segmentation", img)

def main():
	'''
	runs a window with the camera image, a processed image and the trackbars for
	the inRange
	'''
	global current_img

	print ("Write the path for your video, 0 to use default webcam")
	path = raw_input()
	if (path == '0'):
		path = int(0)
	video = cv2.VideoCapture(path)
	print ("At runtime you can press r to use BGR range\n"+
		   "h to use HSV, esc to exit, and space to pause the video.\n"+
		   "Now press Enter to continue ...")
	raw_input()

	# Important windows
	cv2.namedWindow("Bars")
	cv2.namedWindow("Segmentation")
	cv2.namedWindow("Video")

	pause = False

	cv2.createTrackbar("min_channel1", "Bars", 0, 254, nothing)
	cv2.createTrackbar("max_channel1", "Bars", 255, 255, nothing)

	cv2.createTrackbar("min_channel2", "Bars", 0, 254, nothing)
	cv2.createTrackbar("max_channel2", "Bars", 255, 255, nothing)

	cv2.createTrackbar("min_channel3", "Bars", 0, 254, nothing)
	cv2.createTrackbar("max_channel3", "Bars", 255, 255, nothing)

	while(True):

		if(not pause):
			ret, current_img = video.read()
			if not ret:
				break
			cv2.imshow("Video", current_img)

		new_range()
		key = cv2.waitKey(33)
		if key == ord(' '):
			pause = not pause
			print ("Video paused")
		elif key == ord('r'):
			option_rgb = True
			print ("Now using BGR range")
		elif key == ord('h'):
			option_rgb = False
			print ("Now using HSV range")
		elif key == 27:
			break

	video.release()
	cv2.destroyAllWindows()

if __name__ == '__main__':
	main()


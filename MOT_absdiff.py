import cv2
import numpy as np
from MOT_constants import *


def absdiff_ops_on_frame(frame, gray_frame, THRESHOLD_SENSITIVITY):
	gray_frame_new = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	diff_frame = cv2.absdiff(gray_frame, gray_frame_new)
	diff_frame = cv2.blur(diff_frame, (BLUR_SIZE, BLUR_SIZE))
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
	diff_frame = cv2.erode(diff_frame, kernel, iterations=1)
	diff_frame = cv2.dilate(diff_frame, kernel, iterations=3)

	ret, thresh = cv2.threshold(diff_frame, THRESHOLD_SENSITIVITY, 255, cv2.THRESH_BINARY)
	gray_frame = gray_frame_new

	return (gray_frame, diff_frame, thresh)


def absdiff_ops_on_conts(frame, x, y, w, h, c_x, c_y, rot_box_points, rot_c_x, rot_c_y, SHOW_RECT, SHOW_ROT_RECT, largest_area_cont):
	cv2.drawContours(frame, largest_area_cont, -1, CV_CYAN, LINE_THICKNESS)

	if SHOW_RECT:
		cv2.rectangle(frame, (x, y), (x+w, y+h), CV_BLUE, LINE_THICKNESS)
		cv2.circle(frame, (c_x, c_y), CIRCLE_SIZE, CV_BLUE, -1)

	if SHOW_ROT_RECT:
		cv2.drawContours(frame, np.int0([rot_box_points]), -1, CV_RED, LINE_THICKNESS)
		cv2.circle(frame, (rot_c_x, rot_c_y), CIRCLE_SIZE, CV_RED, -1)


def show_absdiff_windows(diff_frame, thresh):
	cv2.imshow("difference", diff_frame)
	cv2.imshow("threshold", thresh)


def destroy_absdiff_windows():
	try:
		cv2.destroyWindow("difference")
		cv2.destroyWindow("threshold")
	except:
		pass
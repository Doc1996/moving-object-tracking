import cv2
import numpy as np
from MOT_constants import *


def backproject_ops_with_select(frame, bounding_roi, bounding_box):
	hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	hsv_roi = hsv_frame[bounding_roi[1]:bounding_roi[3], bounding_roi[0]:bounding_roi[2]]

	lower_hsv_value = np.array([0, 50, 50], dtype="uint8")
	upper_hsv_value = np.array([180, 255, 255], dtype="uint8")

	mask = cv2.inRange(hsv_frame, lower_hsv_value, upper_hsv_value)
	mask_roi = mask[bounding_roi[1]:bounding_roi[3], bounding_roi[0]:bounding_roi[2]]

	hist_roi = cv2.calcHist([hsv_roi], [0, 1], None, [16, 16], [0, 180, 0, 255])  # None or mask_roi
	hist_roi = cv2.normalize(hist_roi, hist_roi, 0, 255, cv2.NORM_MINMAX)

	return (hist_roi, mask, bounding_box)


def backproject_ops_on_frame(frame, hist_roi, mask, bounding_box, THRESHOLD_SENSITIVITY):
	hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	backproject = cv2.calcBackProject([hsv_frame], [0, 1], hist_roi, [0, 180, 0, 255], 1)
	backproject = cv2.medianBlur(backproject, 5)
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
	backproject = cv2.erode(backproject, kernel, iterations=1)
	backproject = cv2.dilate(backproject, kernel, iterations=1)
	ret, thresh = cv2.threshold(backproject, float(THRESHOLD_SENSITIVITY)/20, 255, cv2.THRESH_BINARY)
	thresh = cv2.dilate(thresh, kernel, iterations=3)

	return (backproject, thresh)


def backproject_ops_on_conts(frame, x, y, w, h, c_x, c_y, rot_box_points, rot_c_x, rot_c_y, SHOW_RECT, SHOW_ROT_RECT, backproject, largest_area_cont):
		if SHOW_RECT:
			cv2.rectangle(frame, (x, y), (x+w, y+h), CV_BLUE, LINE_THICKNESS)
			cv2.circle(frame, (c_x, c_y), CIRCLE_SIZE, CV_BLUE, -1)

		if SHOW_ROT_RECT:
			cv2.drawContours(frame, np.int0([rot_box_points]), -1, CV_RED, LINE_THICKNESS)
			cv2.circle(frame, (rot_c_x, rot_c_y), CIRCLE_SIZE, CV_RED, -1)


def show_backproject_windows(backproject, thresh):
	cv2.imshow("backproject", backproject)
	cv2.imshow("threshold", thresh)


def destroy_backproject_windows():
	try:
		cv2.destroyWindow("backproject")
		cv2.destroyWindow("threshold")
	except:
		pass

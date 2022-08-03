import cv2
import numpy as np
from MOT_constants import *


def h_s_and_v(cand, lower_or_upper, change, limit):
	if lower_or_upper == "lower":
		if cand - change <= limit:
			real = limit
		else:
			real = cand - change
	elif lower_or_upper == "upper":
		if cand + change >= limit:
			real = limit
		else:
			real = cand + change

	return real


def hsv_ops_with_select(frame, h_s_and_v, TRACKING_MODE, point=None, bounding_roi=None):
	if TRACKING_MODE == "hsv point":
		(b_var, g_var, r_var) = frame[point[1], point[0]]
	elif TRACKING_MODE == "hsv box":
		roi = frame[bounding_roi[1]:bounding_roi[3], bounding_roi[0]:bounding_roi[2]]
		(b_var, g_var, r_var, channels_var) = cv2.mean(roi)

	color_var = np.array([[[b_var, g_var, r_var]]], dtype="uint8")
	hsv_var = cv2.cvtColor(color_var, cv2.COLOR_BGR2HSV)

	return (b_var, g_var, r_var, hsv_var)


def hsv_ops_on_frame(frame, hsv_var, DELTA_H, DELTA_S, DELTA_V, THRESHOLD_SENSITIVITY):
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	h_cand = int(hsv_var[0][0][0])
	s_cand = int(hsv_var[0][0][1])
	v_cand = int(hsv_var[0][0][2])

	lower_h = h_s_and_v(h_cand, "lower", DELTA_H, 0)  ##
	lower_s = h_s_and_v(s_cand, "lower", DELTA_S, 50)  ##
	lower_v = h_s_and_v(v_cand, "lower", DELTA_V, 50)  ##
	upper_h = h_s_and_v(h_cand, "upper", DELTA_H, 180)  ##
	upper_s = h_s_and_v(s_cand, "upper", DELTA_S, 255)  ##
	upper_v = h_s_and_v(v_cand, "upper", DELTA_V, 255)  ##

	lower_hsv_value = np.array([lower_h, lower_s, lower_v], dtype="uint8")
	upper_hsv_value = np.array([upper_h, upper_s, upper_v], dtype="uint8")

	mask = cv2.inRange(hsv, lower_hsv_value, upper_hsv_value)
	mask = cv2.medianBlur(mask, MEDIAN_BLUR_SIZE)
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
	mask = cv2.erode(mask, kernel, iterations=1)
	mask = cv2.dilate(mask, kernel, iterations=2)

	result = cv2.bitwise_and(frame, frame, mask = mask)
	ret, thresh = cv2.threshold(mask, THRESHOLD_SENSITIVITY, 255, 0)

	return (result, thresh)


def hsv_ops_on_conts(frame, x, y, w, h, c_x, c_y, rot_box_points, rot_c_x, rot_c_y, SHOW_RECT, SHOW_ROT_RECT, result, b_var, g_var, r_var, contours):
	cv2.drawContours(result, contours, -1, (int(b_var), int(g_var), int(r_var)), LINE_THICKNESS)

	if SHOW_RECT:
		cv2.rectangle(frame, (x, y), (x+w, y+h), CV_BLUE, LINE_THICKNESS)
		cv2.circle(frame, (c_x, c_y), CIRCLE_SIZE, CV_BLUE, -1)
		cv2.rectangle(result, (x, y), (x+w, y+h), CV_BLUE, LINE_THICKNESS)
		cv2.circle(result, (c_x, c_y), CIRCLE_SIZE, CV_BLUE, -1)

	if SHOW_ROT_RECT:
		cv2.drawContours(frame, np.int0([rot_box_points]), -1, CV_RED, LINE_THICKNESS)
		cv2.circle(frame, (rot_c_x, rot_c_y), CIRCLE_SIZE, CV_RED, -1)
		cv2.drawContours(result, np.int0([rot_box_points]), -1, CV_RED, LINE_THICKNESS)
		cv2.circle(result, (rot_c_x, rot_c_y), CIRCLE_SIZE, CV_RED, -1)	


def show_hsv_windows(result, thresh):
	cv2.imshow("result", result)
	cv2.imshow("threshold", thresh)


def destroy_hsv_windows():
	try:
		cv2.destroyWindow("result")
		cv2.destroyWindow("threshold")
	except:
		pass
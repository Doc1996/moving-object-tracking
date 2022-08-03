import cv2
import numpy as np
from MOT_constants import *


def draw_flow_frame(flow):
	h, w = flow.shape[:2]
	f_x = flow[ : , : , 0]
	f_y = flow[ : , : , 1]
	angle = np.arctan2(f_y, f_x) + np.pi
	distance = np.sqrt(f_x*f_x + f_y*f_y)
	hsv_flow_frame = np.zeros((h, w, 3), dtype="uint8")
	hsv_flow_frame[..., 0] = angle * float(90)/np.pi
	hsv_flow_frame[..., 1] = 255
	hsv_flow_frame[..., 2] = np.minimum(distance*4, 255)
	flow_frame = cv2.cvtColor(hsv_flow_frame, cv2.COLOR_HSV2BGR)

	return flow_frame


def draw_gray_frame_with_lines(gray_frame, flow):
	h, w = gray_frame.shape[:2]
	y, x = np.mgrid[STEP_SIZE//2:h:STEP_SIZE, STEP_SIZE//2:w:STEP_SIZE].reshape(2, -1).astype(int)
	f_x, f_y = flow[y, x].T
	lines = np.array([x, y, x+f_x, y+f_y]).T.reshape(-1, 2, 2)
	lines = np.int32(lines + 0.5)
	gray_frame_with_lines = cv2.cvtColor(gray_frame, cv2.COLOR_GRAY2BGR)
	cv2.polylines(gray_frame_with_lines, lines, 0, CV_GREEN)

	return gray_frame_with_lines


def opt_flow_ops_on_frame(frame, gray_frame, THRESHOLD_SENSITIVITY):
	gray_frame_new = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

	flow = cv2.calcOpticalFlowFarneback(gray_frame, gray_frame_new, flow=None, pyr_scale=0.5, levels=3, winsize=11, iterations=2, \
		poly_n=2, poly_sigma=1.1, flags=0)
	flow_frame = draw_flow_frame(flow)  ##
	gray_flow_frame = cv2.cvtColor(flow_frame, cv2.COLOR_BGR2GRAY)
	gray_flow_frame = cv2.blur(gray_flow_frame, (BLUR_SIZE, BLUR_SIZE))
	ret, thresh = cv2.threshold(gray_flow_frame, THRESHOLD_SENSITIVITY, 255, cv2.THRESH_BINARY)
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
	thresh = cv2.dilate(thresh, kernel, iterations=1)
	
	gray_frame_with_lines = draw_gray_frame_with_lines(gray_frame, flow)
	gray_frame = gray_frame_new

	return (gray_frame, flow, flow_frame, thresh, gray_frame_with_lines)


def opt_flow_ops_on_conts(frame, x, y, w, h, c_x, c_y, rot_box_points, rot_c_x, rot_c_y, SHOW_RECT, SHOW_ROT_RECT, largest_area_cont):
	cv2.drawContours(frame, largest_area_cont, -1, CV_CYAN, LINE_THICKNESS)

	if SHOW_RECT:
		cv2.rectangle(frame, (x, y), (x+w, y+h), CV_BLUE, LINE_THICKNESS)
		cv2.circle(frame, (c_x, c_y), CIRCLE_SIZE, CV_BLUE, -1)

	if SHOW_ROT_RECT:
		cv2.drawContours(frame, np.int0([rot_box_points]), -1, CV_RED, LINE_THICKNESS)
		cv2.circle(frame, (rot_c_x, rot_c_y), CIRCLE_SIZE, CV_RED, -1)


def show_opt_flow_windows(flow_frame, thresh, gray_frame_with_lines):
	cv2.imshow("optical flow", flow_frame)
	cv2.imshow("threshold", thresh)
	cv2.imshow("gray video with lines", gray_frame_with_lines)


def destroy_opt_flow_windows():
	try:
		cv2.destroyWindow("optical flow")
		cv2.destroyWindow("threshold")
		cv2.destroyWindow("gray video with lines")
	except:
		pass
import cv2
from MOT_constants import *


def tracking_mode_trackbar(trackbar_name, TRACKING_MODE):
	def nothing(trackbar_var):
		pass

	cv2.createTrackbar("track mode", trackbar_name, 0, 4, nothing)
	if TRACKING_MODE == "hsv point": tracking_mode_value = 0
	elif TRACKING_MODE == "hsv box": tracking_mode_value = 1
	elif TRACKING_MODE == "backproject": tracking_mode_value = 2
	elif TRACKING_MODE == "absdiff": tracking_mode_value = 3
	elif TRACKING_MODE == "opt flow": tracking_mode_value = 4
	cv2.setTrackbarPos("track mode", trackbar_name, tracking_mode_value)


def show_rect_trackbar(trackbar_name, SHOW_RECT):
	def nothing(trackbar_var):
		pass

	cv2.createTrackbar("show rect", trackbar_name, 0, 1, nothing)
	if SHOW_RECT == False: rect_value = 0
	elif SHOW_RECT == True: rect_value = 1
	cv2.setTrackbarPos("show rect", trackbar_name, rect_value)


def show_rot_rect_trackbar(trackbar_name, SHOW_ROT_RECT):
	def nothing(trackbar_var):
		pass

	cv2.createTrackbar("show rot r", trackbar_name, 0, 1, nothing)
	if SHOW_ROT_RECT == False: rot_rect_value = 0
	elif SHOW_ROT_RECT == True: rot_rect_value = 1
	cv2.setTrackbarPos("show rot r", trackbar_name, rot_rect_value)


def track_rect_or_rot_rect_trackbar(trackbar_name, TRACK_RECT_OR_ROT_RECT):
	def nothing(trackbar_var):
		pass

	cv2.createTrackbar("target", trackbar_name, 0, 1, nothing)
	if TRACK_RECT_OR_ROT_RECT == "rect": target_value = 0
	elif TRACK_RECT_OR_ROT_RECT == "rot rect": target_value = 1
	cv2.setTrackbarPos("target", trackbar_name, target_value)


def win_size_trackbar(trackbar_name, CAM_WIDTH):
	def nothing(trackbar_var):
		pass

	cv2.createTrackbar("win size", trackbar_name, 0, 1, nothing)
	if CAM_WIDTH == 320: win_size_value = 0
	elif CAM_WIDTH == 640: win_size_value = 1
	cv2.setTrackbarPos("win size", trackbar_name, win_size_value)



def show_side_wins_trackbar(trackbar_name, SHOW_SIDE_WINS):
	def nothing(trackbar_var):
		pass

	cv2.createTrackbar("show side", trackbar_name, 0, 1, nothing)
	if SHOW_SIDE_WINS == False: side_wins_value = 0
	elif SHOW_SIDE_WINS == True: side_wins_value = 1
	cv2.setTrackbarPos("show side", trackbar_name, side_wins_value)


def delta_h_s_and_v_trackbar(trackbar_name, DELTA_H, DELTA_S, DELTA_V):
	def nothing(trackbar_var):
		pass

	cv2.createTrackbar("delta_h/5", trackbar_name, 0, 6, nothing)
	for delta_h_value in range(0, 7):
		if DELTA_H//5 == delta_h_value:
			cv2.setTrackbarPos("delta_h/5", trackbar_name, delta_h_value)

	cv2.createTrackbar("delta_s/10", trackbar_name, 0, 12, nothing)
	for delta_s_value in range(0, 13):
		if DELTA_S//10 == delta_s_value:
			cv2.setTrackbarPos("delta_s/10", trackbar_name, delta_s_value)

	cv2.createTrackbar("delta_v/10", trackbar_name, 0, 12, nothing)
	for delta_v_value in range(0, 13):
		if DELTA_V//10 == delta_v_value:
			cv2.setTrackbarPos("delta_v/10", trackbar_name, delta_v_value)


def threshold_trackbar(trackbar_name, THRESHOLD_SENSITIVITY):
	def nothing(trackbar_var):
		pass

	cv2.createTrackbar("thresh/5", trackbar_name, 0, 10, nothing)
	for threshold_value in range(0, 11):
		if THRESHOLD_SENSITIVITY//5 == threshold_value:
			cv2.setTrackbarPos("thresh/5", trackbar_name, threshold_value)


def servo_pos_trackbar(trackbar_name, STARTING_PULSEWIDTH):
	def nothing(trackbar_var):
		pass

	cv2.createTrackbar("servo pos", trackbar_name, 0, 4, nothing)
	if STARTING_PULSEWIDTH == MIN_PULSEWIDTH: servo_pos_value = 0
	elif STARTING_PULSEWIDTH == MED_MIN_PULSEWIDTH: servo_pos_value = 1
	elif STARTING_PULSEWIDTH == MED_PULSEWIDTH: servo_pos_value = 2
	elif STARTING_PULSEWIDTH == MED_MAX_PULSEWIDTH: servo_pos_value = 3
	elif STARTING_PULSEWIDTH == MAX_PULSEWIDTH: servo_pos_value = 4
	cv2.setTrackbarPos("servo pos", trackbar_name, servo_pos_value)


def servo_speed_trackbar(trackbar_name, LARGE_SPEED_FACTOR):
	def nothing(trackbar_var):
		pass

	cv2.createTrackbar("servo speed", trackbar_name, 0, 4, nothing)
	if TRACKING_MODE in ("hsv point", "hsv box", "backproject"):
		if LARGE_SPEED_FACTOR == 0: large_servo_speed_value = 0
		elif LARGE_SPEED_FACTOR == 0.06: large_servo_speed_value = 1
		elif LARGE_SPEED_FACTOR == 0.08: large_servo_speed_value = 2
		elif LARGE_SPEED_FACTOR == 0.1: large_servo_speed_value = 3
		elif LARGE_SPEED_FACTOR == 0.12: large_servo_speed_value = 4
	elif TRACKING_MODE in ("absdiff", "opt flow"):
		if LARGE_SPEED_FACTOR == 0: large_servo_speed_value = 0
		elif LARGE_SPEED_FACTOR == 0.1: large_servo_speed_value = 1
		elif LARGE_SPEED_FACTOR == 0.12: large_servo_speed_value = 2
		elif LARGE_SPEED_FACTOR == 0.14: large_servo_speed_value = 3
		elif LARGE_SPEED_FACTOR == 0.16: large_servo_speed_value = 4
	cv2.setTrackbarPos("servo speed", trackbar_name, large_servo_speed_value)
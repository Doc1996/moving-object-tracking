import cv2
from MOT_constants import *


def  get_tracking_mode_trackbar(trackbar_name):
	get_tracking_mode_value = cv2.getTrackbarPos("track mode", trackbar_name)
	if get_tracking_mode_value == 0: TRACKING_MODE = "hsv point"
	elif get_tracking_mode_value == 1: TRACKING_MODE = "hsv box"
	elif get_tracking_mode_value == 2: TRACKING_MODE = "backproject"
	elif get_tracking_mode_value == 3: TRACKING_MODE = "absdiff"
	elif get_tracking_mode_value == 4: TRACKING_MODE = "opt flow"

	return TRACKING_MODE


def get_show_rect_trackbar(trackbar_name):
	get_rect_value = cv2.getTrackbarPos("show rect", trackbar_name)
	if get_rect_value == 0: SHOW_RECT = False
	elif get_rect_value == 1: SHOW_RECT = True

	return SHOW_RECT


def get_show_rot_rect_trackbar(trackbar_name):
	get_rot_rect_value = cv2.getTrackbarPos("show rot r", trackbar_name)
	if get_rot_rect_value == 0: SHOW_ROT_RECT = False
	elif get_rot_rect_value == 1: SHOW_ROT_RECT = True

	return SHOW_ROT_RECT


def get_track_rect_or_rot_rect_trackbar(trackbar_name):
	get_target_value = cv2.getTrackbarPos("target", trackbar_name)
	if get_target_value == 0: TRACK_RECT_OR_ROT_RECT = "rect"
	elif get_target_value == 1: TRACK_RECT_OR_ROT_RECT = "rot rect"

	return TRACK_RECT_OR_ROT_RECT


def get_win_size_trackbar(trackbar_name):
	get_win_size_value = cv2.getTrackbarPos("win size", trackbar_name)
	if get_win_size_value == 0: CAM_WIDTH = 320
	elif get_win_size_value == 1: CAM_WIDTH = 640

	return CAM_WIDTH


def get_show_side_wins_trackbar(trackbar_name):
	get_side_wins_value = cv2.getTrackbarPos("show side", trackbar_name)
	if get_side_wins_value == 0: SHOW_SIDE_WINS = False
	elif get_side_wins_value == 1: SHOW_SIDE_WINS = True

	return SHOW_SIDE_WINS


def get_delta_h_s_and_v_trackbar(trackbar_name):
	get_delta_h_value = cv2.getTrackbarPos("delta_h/5", trackbar_name)
	for iterator in range(0, 7):
		if get_delta_h_value == iterator:
			DELTA_H = iterator*5

	get_delta_v_value = cv2.getTrackbarPos("delta_s/10", trackbar_name)
	for iterator in range(0, 13):
		if get_delta_v_value == iterator:
			DELTA_S = iterator*10

	get_delta_v_value = cv2.getTrackbarPos("delta_v/10", trackbar_name)
	for iterator in range(0, 13):
		if get_delta_v_value == iterator:
			DELTA_V = iterator*10

	return (DELTA_H, DELTA_S, DELTA_V)


def get_threshold_trackbar(trackbar_name):
	get_threshold_value = cv2.getTrackbarPos("thresh/5", trackbar_name)
	for iterator in range(0, 11):
		if get_threshold_value == iterator:
			THRESHOLD_SENSITIVITY = iterator*5

	return THRESHOLD_SENSITIVITY


def get_servo_pos_trackbar(trackbar_name):
	get_servo_pos = cv2.getTrackbarPos("servo pos", trackbar_name)
	if get_servo_pos == 0: STARTING_PULSEWIDTH = MIN_PULSEWIDTH
	elif get_servo_pos == 1: STARTING_PULSEWIDTH = MED_MIN_PULSEWIDTH
	elif get_servo_pos == 2: STARTING_PULSEWIDTH = MED_PULSEWIDTH
	elif get_servo_pos == 3: STARTING_PULSEWIDTH = MED_MAX_PULSEWIDTH
	elif get_servo_pos == 4: STARTING_PULSEWIDTH = MAX_PULSEWIDTH

	return STARTING_PULSEWIDTH


def get_servo_speed_trackbar(trackbar_name):
	get_large_servo_speed = cv2.getTrackbarPos("servo speed", trackbar_name)
	if TRACKING_MODE in ("hsv point", "hsv box", "backproject"):
		if get_large_servo_speed == 0: LARGE_SPEED_FACTOR = 0
		elif get_large_servo_speed == 1: LARGE_SPEED_FACTOR = 0.06
		elif get_large_servo_speed == 2: LARGE_SPEED_FACTOR = 0.08
		elif get_large_servo_speed == 3: LARGE_SPEED_FACTOR = 0.1
		elif get_large_servo_speed == 4: LARGE_SPEED_FACTOR = 0.12
	elif TRACKING_MODE in ("absdiff", "opt flow"):
		if get_large_servo_speed == 0: LARGE_SPEED_FACTOR = 0
		elif get_large_servo_speed == 1: LARGE_SPEED_FACTOR = 0.1
		elif get_large_servo_speed == 2: LARGE_SPEED_FACTOR = 0.12
		elif get_large_servo_speed == 3: LARGE_SPEED_FACTOR = 0.14
		elif get_large_servo_speed == 4: LARGE_SPEED_FACTOR = 0.16

	return LARGE_SPEED_FACTOR
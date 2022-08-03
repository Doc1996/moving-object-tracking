import cv2
import time

from MOT_constants import *
from MOT_webcam import *
from MOT_mouse import *
from MOT_get_fps import get_fps
from MOT_set_trackbar import *
from MOT_get_trackbar import *
from MOT_univ_contours import univ_ops_on_conts
from MOT_hsv import *
from MOT_backproject import *
from MOT_absdiff import *
from MOT_opt_flow import *


if STARTED_ON_RASPBERRY_PI:
	import pigpio
	from subprocess import call

	from MOT_servo_move import move_servo



t = 0
pulsewidth = STARTING_PULSEWIDTH
frame_count = 0
loop_fps = 0
start_time = time.time()

if STARTED_ON_RASPBERRY_PI:
	call("sudo pigpiod", shell=True)
	call("sudo pigpiod", shell=True)
	servo = pigpio.pi()
else:
	servo = None


wvs = WebcamVideoStream(CAM_SOURCE, CAM_WIDTH, CAM_HEIGHT).start()
ret, frame = wvs.read()
frame = cv2.flip(frame, FLIP_HORIZONTALLY)

gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

m = Mouse(frame)
cv2.namedWindow("video")
cv2.namedWindow("side trackbar")
cv2.namedWindow("main trackbar")

tracking_mode_trackbar("main trackbar", TRACKING_MODE)
show_rect_trackbar("main trackbar", SHOW_RECT)
show_rot_rect_trackbar("main trackbar", SHOW_ROT_RECT)
win_size_trackbar("side trackbar", CAM_WIDTH)
show_side_wins_trackbar("side trackbar", SHOW_SIDE_WINS)
delta_h_s_and_v_trackbar("side trackbar", DELTA_H, DELTA_S, DELTA_V)
threshold_trackbar("side trackbar", THRESHOLD_SENSITIVITY)

if STARTED_ON_RASPBERRY_PI:
	track_rect_or_rot_rect_trackbar("main trackbar", TRACK_RECT_OR_ROT_RECT)
	servo_pos_trackbar("main trackbar", STARTING_PULSEWIDTH)
	servo_speed_trackbar("main trackbar", LARGE_SPEED_FACTOR)


try:
	while True:
		ret, frame = wvs.read()
		frame = cv2.flip(frame, FLIP_HORIZONTALLY)
		m.frame = frame

		gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

		if TRACKING_MODE in ("hsv point", "absdiff", "opt flow"):
			cv2.setMouseCallback("video", m.select_point)
		elif TRACKING_MODE in ("hsv box", "backproject"):
			cv2.setMouseCallback("video", m.select_box)

		if STARTED_ON_RASPBERRY_PI:
			servo.set_servo_pulsewidth(SERVO_PIN, STARTING_PULSEWIDTH)

		if m.track:
			largest_area_list = []
			center_list = (None, None, None, None)
			center_counter = 0
			servo_counter = SERVO_COUNTER_LIMIT

			if TRACKING_MODE == "hsv point":
				(b_var, g_var, r_var, hsv_var) = hsv_ops_with_select(frame, h_s_and_v, TRACKING_MODE, point=m.point)
			elif TRACKING_MODE == "backproject":
				(hist_roi, mask, bounding_box) = backproject_ops_with_select(frame, m.bounding_roi, m.bounding_box)
			elif TRACKING_MODE ==  "hsv box":
				(b_var, g_var, r_var, hsv_var) = hsv_ops_with_select(frame, h_s_and_v, TRACKING_MODE, bounding_roi=m.bounding_roi)


		while m.track:
			ret, frame = wvs.read()
			frame = cv2.flip(frame, FLIP_HORIZONTALLY)
			m.frame = frame
	
			if TRACKING_MODE in ("hsv point", "hsv box"):
				(result, thresh) = hsv_ops_on_frame(frame, hsv_var, DELTA_H, DELTA_S, DELTA_V, THRESHOLD_SENSITIVITY)
			elif TRACKING_MODE == "backproject":
				(backproject, thresh) = backproject_ops_on_frame(frame, hist_roi, mask, bounding_box, THRESHOLD_SENSITIVITY)
			elif TRACKING_MODE == "absdiff":
				(gray_frame, diff_frame, thresh) = absdiff_ops_on_frame(frame, gray_frame, THRESHOLD_SENSITIVITY)
			elif TRACKING_MODE == "opt flow":
				(gray_frame, flow, flow_frame, thresh, gray_frame_with_lines) = opt_flow_ops_on_frame(frame, gray_frame, THRESHOLD_SENSITIVITY)

			if TRACKING_MODE in ("hsv point", "hsv box"):
				(largest_area_list, center_list, center_counter, servo_counter, pulsewidth, t) = univ_ops_on_conts(frame, thresh, largest_area_list, center_list, center_counter, servo_counter, pulsewidth, t, servo, \
					TRACKING_MODE, SHOW_RECT, SHOW_ROT_RECT, TRACK_RECT_OR_ROT_RECT, CAM_WIDTH, CAM_HEIGHT, LARGE_SPEED_FACTOR, SMALL_SPEED_FACTOR, result, b_var, g_var, r_var)
			elif TRACKING_MODE == "backproject":
				(largest_area_list, center_list, center_counter, servo_counter, pulsewidth, t) = univ_ops_on_conts(frame, thresh, largest_area_list, center_list, center_counter, servo_counter, pulsewidth, t, servo, \
					TRACKING_MODE, SHOW_RECT, SHOW_ROT_RECT, TRACK_RECT_OR_ROT_RECT, CAM_WIDTH, CAM_HEIGHT, LARGE_SPEED_FACTOR, SMALL_SPEED_FACTOR, backproject)
			elif TRACKING_MODE in ("absdiff", "opt flow"):
				(largest_area_list, center_list, center_counter, servo_counter, pulsewidth, t) = univ_ops_on_conts(frame, thresh, largest_area_list, center_list, center_counter, servo_counter, pulsewidth, t, servo, \
					TRACKING_MODE, SHOW_RECT, SHOW_ROT_RECT, TRACK_RECT_OR_ROT_RECT, CAM_WIDTH, CAM_HEIGHT, LARGE_SPEED_FACTOR, SMALL_SPEED_FACTOR)

			(start_time, frame_count, loop_fps) = get_fps(start_time, frame_count, loop_fps)

			cv2.putText(frame, ("tracking mode: {} (ON)".format(TRACKING_MODE)), (10, 25), cv2.FONT_HERSHEY_SIMPLEX,  TEXT_SIZE, CV_RED, LINE_THICKNESS//2)
			if loop_fps <= 30:
				cv2.putText(frame, ("FPS: {}".format(loop_fps)), (10, CAM_HEIGHT-15), cv2.FONT_HERSHEY_SIMPLEX,  TEXT_SIZE, CV_RED, LINE_THICKNESS//2)
			else:
				cv2.putText(frame, ("FPS: 30.0 ({})".format(loop_fps)), (10, CAM_HEIGHT-15), cv2.FONT_HERSHEY_SIMPLEX,  TEXT_SIZE, CV_RED, LINE_THICKNESS//2)
	
			if TRACKING_MODE in ("hsv point", "hsv box"):
				cv2.rectangle(frame, (CAM_WIDTH-38, 35), (CAM_WIDTH-18, 15), (int(b_var), int(g_var), int(r_var)), -1)
				cv2.rectangle(frame, (CAM_WIDTH-38, 35), (CAM_WIDTH-18, 15), CV_RED, LINE_THICKNESS//2)
	
			cv2.imshow("video", frame)
	
			if SHOW_SIDE_WINS:
				if TRACKING_MODE in ("hsv point", "hsv box"): show_hsv_windows(result, thresh)
				elif TRACKING_MODE == "backproject": show_backproject_windows(backproject, thresh)
				elif TRACKING_MODE == "absdiff": show_absdiff_windows(diff_frame, thresh)
				elif TRACKING_MODE == "opt flow": show_opt_flow_windows(flow_frame, thresh, gray_frame_with_lines)
			else:
				if TRACKING_MODE in ("hsv point", "hsv box"): destroy_hsv_windows()
				elif TRACKING_MODE == "backproject": destroy_backproject_windows()
				elif TRACKING_MODE == "absdiff": destroy_absdiff_windows()
				elif TRACKING_MODE == "opt flow": destroy_opt_flow_windows()
	
			SHOW_RECT = get_show_rect_trackbar("main trackbar")
			SHOW_ROT_RECT = get_show_rot_rect_trackbar("main trackbar")
			SHOW_SIDE_WINS = get_show_side_wins_trackbar("side trackbar")
			(DELTA_H, DELTA_S, DELTA_V) = get_delta_h_s_and_v_trackbar("side trackbar")
			THRESHOLD_SENSITIVITY = get_threshold_trackbar("side trackbar")
	
			if STARTED_ON_RASPBERRY_PI:
				TRACK_RECT_OR_ROT_RECT = get_track_rect_or_rot_rect_trackbar("main trackbar")

			if cv2.waitKey(MIN_FRAME_TIME) == KEY_ESC:
				raise KeyboardInterrupt


		if not m.track:
			(start_time, frame_count, loop_fps) = get_fps(start_time, frame_count, loop_fps)

			if TRACKING_MODE in ("hsv point", "hsv box"): destroy_hsv_windows()
			elif TRACKING_MODE == "backproject": destroy_backproject_windows()
			elif TRACKING_MODE == "absdiff": destroy_absdiff_windows()
			elif TRACKING_MODE == "opt flow": destroy_opt_flow_windows()

			cv2.putText(frame, ("tracking mode: {} (OFF)".format(TRACKING_MODE)), (10, 25), cv2.FONT_HERSHEY_SIMPLEX,  TEXT_SIZE, CV_RED, LINE_THICKNESS//2)
			if loop_fps <= 30:
				cv2.putText(frame, ("FPS: {}".format(loop_fps)), (10, CAM_HEIGHT-15), cv2.FONT_HERSHEY_SIMPLEX,  TEXT_SIZE, CV_RED, LINE_THICKNESS//2)
			else:
				cv2.putText(frame, ("FPS: 30.0 ({})".format(loop_fps)), (10, CAM_HEIGHT-15), cv2.FONT_HERSHEY_SIMPLEX,  TEXT_SIZE, CV_RED, LINE_THICKNESS//2)

			cv2.imshow("video", frame)

			TRACKING_MODE = get_tracking_mode_trackbar("main trackbar")

			if not STARTED_ON_RASPBERRY_PI:
				if get_win_size_trackbar("side trackbar") != CAM_WIDTH:
					cv2.destroyWindow("video")
					CAM_WIDTH = get_win_size_trackbar("side trackbar")
					CAM_HEIGHT = int(CAM_WIDTH * 0.75)
					wvs.stop()
					wvs.stream.release()
					wvs = WebcamVideoStream(CAM_SOURCE, CAM_WIDTH, CAM_HEIGHT).start()
			
			if STARTED_ON_RASPBERRY_PI:
				STARTING_PULSEWIDTH = get_servo_pos_trackbar("main trackbar")
				pulsewidth = STARTING_PULSEWIDTH
				LARGE_SPEED_FACTOR = get_servo_speed_trackbar("main trackbar")
				SMALL_SPEED_FACTOR = LARGE_SPEED_FACTOR * 0.5

			if cv2.waitKey(MIN_FRAME_TIME) == KEY_ESC:
				raise KeyboardInterrupt


except KeyboardInterrupt:
	if STARTED_ON_RASPBERRY_PI:
		servo.stop()

	wvs.stop()
	wvs.stream.release()
	cv2.destroyAllWindows()
import cv2

from MOT_constants import *
from MOT_hsv import hsv_ops_on_conts
from MOT_backproject import backproject_ops_on_conts
from MOT_absdiff import absdiff_ops_on_conts


if STARTED_ON_RASPBERRY_PI:
	from MOT_servo_move import move_servo



def univ_ops_on_conts(frame, thresh, largest_area_list, center_list, center_counter, servo_counter, pulsewidth, t, servo, TRACKING_MODE, SHOW_RECT, SHOW_ROT_RECT, \
		TRACK_RECT_OR_ROT_RECT, CAM_WIDTH, CAM_HEIGHT, LARGE_SPEED_FACTOR, SMALL_SPEED_FACTOR, result=None, b_var=None, g_var=None, r_var=None, backproject=None):

	(c_x_ref, c_y_ref, rot_c_x_ref, rot_c_y_ref) = center_list

	contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	contours = [i for i in contours if cv2.contourArea(i)>=MIN_AREA]

	if contours and servo_counter >= SERVO_COUNTER_LIMIT:
		largest_area_cont = max(contours, key=cv2.contourArea)
		largest_area = cv2.contourArea(largest_area_cont)

		if largest_area <= CAM_WIDTH * CAM_HEIGHT * CONTOUR_AREA_FACTOR:
			largest_area_list.append(largest_area)

			if len(largest_area_list) >= LOW_LIST_LEN_LIMIT:
				largest_area_sum = sum(largest_area_list)
				largest_area_average = largest_area_sum / len(largest_area_list)

				if MIN_LARGEST_AREA_AVG_FACTOR < largest_area/largest_area_average < MAX_LARGEST_AREA_AVG_FACTOR:
					area_counter = 0
					for list_el in largest_area_list:
						if MIN_LARGEST_AREA_EL_FACTOR < largest_area/list_el < MAX_LARGEST_AREA_EL_FACTOR:
							area_counter += 1

					if area_counter >= AREA_AND_CENTER_COUNTER_LIMIT:
						(x, y, w, h) = cv2.boundingRect(largest_area_cont)
						c_x = x+w//2
						c_y = y+h//2
						rot_bounding_box = cv2.minAreaRect(largest_area_cont)
						rot_w = rot_bounding_box[1][0]
						rot_h = rot_bounding_box[1][1]

						if STARTED_ON_RASPBERRY_PI:
							rot_box_points = cv2.cv.BoxPoints(rot_bounding_box)
						else:
							rot_box_points = cv2.boxPoints(rot_bounding_box)

						rot_c_x = int(rot_box_points[0][0]+rot_box_points[2][0])//2
						rot_c_y = int(rot_box_points[1][1]+rot_box_points[3][1])//2


						if (c_x_ref or c_y_ref or rot_c_x_ref or rot_c_y_ref) == None:
							(c_x_ref, c_y_ref, rot_c_x_ref, rot_c_y_ref) = (c_x, c_y, rot_c_x, rot_c_y)
							center_counter = 0
						elif (w * h) <= CAM_WIDTH * CAM_HEIGHT * BOUNDING_AREA_FACTOR and rot_w >= MIN_WIDTH_OR_HEIGHT and rot_h >= MIN_WIDTH_OR_HEIGHT \
								and abs(c_x-c_x_ref) <= CAM_WIDTH//3 and abs(rot_c_x-rot_c_x_ref) <= CAM_WIDTH//3 \
								and abs(c_y-c_y_ref) <= CAM_HEIGHT//3 and abs(rot_c_y-rot_c_y_ref) <= CAM_HEIGHT//3:
							univ_contours_vars = (frame, x, y, w, h, c_x, c_y, rot_box_points, rot_c_x, rot_c_y, SHOW_RECT, SHOW_ROT_RECT)

							if TRACKING_MODE in ("hsv point", "hsv box"):
								hsv_ops_on_conts(frame, x, y, w, h, c_x, c_y, rot_box_points, rot_c_x, rot_c_y, SHOW_RECT, SHOW_ROT_RECT, result, b_var, g_var, r_var, contours)
							elif TRACKING_MODE == "backproject":
								backproject_ops_on_conts(frame, x, y, w, h, c_x, c_y, rot_box_points, rot_c_x, rot_c_y, SHOW_RECT, SHOW_ROT_RECT, backproject, largest_area_cont)
							elif TRACKING_MODE in ("absdiff", "opt flow"):
								absdiff_ops_on_conts(frame, x, y, w, h, c_x, c_y, rot_box_points, rot_c_x, rot_c_y, SHOW_RECT, SHOW_ROT_RECT, largest_area_cont)

							if STARTED_ON_RASPBERRY_PI:
								(pulsewidth, t) = move_servo(c_x, rot_c_x, pulsewidth, t, servo, TRACK_RECT_OR_ROT_RECT, CAM_WIDTH, LARGE_SPEED_FACTOR, SMALL_SPEED_FACTOR)
								servo_counter = 0
							else:
								servo_counter = SERVO_COUNTER_LIMIT

							(c_x_ref, c_y_ref, rot_c_x_ref, rot_c_y_ref) = (c_x, c_y, rot_c_x, rot_c_y)
							center_counter = 0

						elif center_counter >= AREA_AND_CENTER_COUNTER_LIMIT:
							(c_x_ref, c_y_ref, rot_c_x_ref, rot_c_y_ref) = (None, None, None, None)
						else:
							center_counter += 1

	if len(largest_area_list) >= HIGH_LIST_LEN_LIMIT:
		del largest_area_list[0]

	servo_counter += 1
	center_list = (c_x_ref, c_y_ref, rot_c_x_ref, rot_c_y_ref)

	if contours and servo_counter >= SERVO_COUNTER_LIMIT and TRACKING_MODE == "absdiff":
		cv2.drawContours(frame, contours, -1, CV_GREEN, LINE_THICKNESS//2)

	return (largest_area_list, center_list, center_counter, servo_counter, pulsewidth, t)
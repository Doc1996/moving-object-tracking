from MOT_constants import *


def move_servo(c_x, rot_c_x, pulsewidth, t, servo, TRACK_RECT_OR_ROT_RECT, CAM_WIDTH, LARGE_SPEED_FACTOR, SMALL_SPEED_FACTOR):
	if TRACK_RECT_OR_ROT_RECT == "rect": target_x = c_x
	elif TRACK_RECT_OR_ROT_RECT == "rot rect": target_x = rot_c_x

	pw_per_width = round(float(MAX_PULSEWIDTH - MIN_PULSEWIDTH) / CAM_WIDTH, 3)
	delta_width = target_x - CAM_WIDTH//2

	if abs(delta_width) >= CAM_WIDTH//12:
		speed_factor = LARGE_SPEED_FACTOR
	else:
		speed_factor = SMALL_SPEED_FACTOR

	delta_width = - delta_width

	if delta_width < 0:
		if target_x < - FRAME_BORDER_BUFFER:
			pulsewidth = MED_PULSEWIDTH; t = 0
		else:
			pulsewidth = pulsewidth + delta_width * pw_per_width * speed_factor
			if pulsewidth <= MIN_PULSEWIDTH:
				pulsewidth = MIN_PULSEWIDTH; t += 1
			else:
				t = 0
	elif delta_width > 0:
		if target_x > (CAM_WIDTH + FRAME_BORDER_BUFFER):
			pulsewidth = MED_PULSEWIDTH; t = 0
		else:
			pulsewidth = pulsewidth + delta_width * pw_per_width * speed_factor
			if pulsewidth >= MAX_PULSEWIDTH:
				pulsewidth = MAX_PULSEWIDTH; t += 1
			else:
				t = 0

	if t == 50:
		pulsewidth = MED_PULSEWIDTH; t = 0

	servo.set_servo_pulsewidth(SERVO_PIN, pulsewidth)

	print("pw: {}, c_x: {}, delta_width: {}".format(int(round(pulsewidth)), target_x, int(delta_width)))

	return (pulsewidth, t)
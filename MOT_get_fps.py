import time
from MOT_constants import *


def get_fps(start_time, frame_count, loop_fps):
	if frame_count >= FRAME_COUNTER:
		duration = float(time.time() - start_time)
		loop_fps = float(frame_count / duration)
		duration = round(duration, 1)
		loop_fps = round(loop_fps, 1)
		frame_count = 0
		start_time = time.time()
	else:
		frame_count += 1

	return (start_time, frame_count, loop_fps)
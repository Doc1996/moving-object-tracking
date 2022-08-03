import cv2
from MOT_constants import *


class Mouse:

	def __init__(self, frame):
		self.frame = frame
		self.track = False
		self.point = None
		self.box_p1 = None
		self.box_p2 = None
		self.box_drag = False
		self.bounding_box = None
		self.bounding_roi = None


	def select_point(self, event, p_x, p_y, flags, params):
		if event == cv2.EVENT_LBUTTONDOWN:
			self.track = True
			self.point = (p_x, p_y)
		if event == cv2.EVENT_RBUTTONDOWN:
			self.track = False
			self.point = None


	def select_box(self, event, p_x, p_y, flags, params):
		if event == cv2.EVENT_LBUTTONDOWN and not self.box_drag:
			self.box_p1 = (p_x, p_y)
			self.box_drag = True
		elif event == cv2.EVENT_MOUSEMOVE and self.box_drag:
			cv2.rectangle(self.frame, self.box_p1, (p_x, p_y), CV_BLUE, LINE_THICKNESS)
		elif event == cv2.EVENT_LBUTTONUP and self.box_drag:
			self.box_p2 = (p_x, p_y)
			if self.box_p2[0] == self.box_p1[0] or self.box_p2[1] == self.box_p1[1]:
				self.box_p1 = None
				self.box_p2 = None
			else:
				self.track = True
			self.box_drag = False

		if event == cv2.EVENT_RBUTTONDOWN:
			self.track = False
			self.bounding_box = None
			self.bounding_roi = None

		if self.box_p1 and self.box_p2:
			x_min = min((self.box_p1[0], self.box_p2[0]))
			x_max = max((self.box_p1[0], self.box_p2[0]))
			y_min = min((self.box_p1[1], self.box_p2[1]))
			y_max = max((self.box_p1[1], self.box_p2[1]))
			self.bounding_box = (x_min, y_min, x_max-x_min, y_max-y_min)
			self.bounding_roi = (x_min, y_min, x_max, y_max)

		cv2.imshow("video", self.frame)
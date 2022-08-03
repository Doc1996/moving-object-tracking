import cv2
from threading import Thread
from MOT_constants import *


class WebcamVideoStream:

	def __init__(self, CAM_SOURCE, CAM_WIDTH, CAM_HEIGHT):
		self.source = CAM_SOURCE
		self.width = CAM_WIDTH
		self.height = CAM_HEIGHT
		self.stopped = False
		self.stream = cv2.VideoCapture(self.source)
		self.stream.set(3, self.width)
		self.stream.set(4, self.height)
		(self.grabbed, self.frame) = self.stream.read()


	def start(self):
		self.stopped = False
		t = Thread(target=self.update, args=())
		t.daemon = True
		t.start()
		return self


	def update(self):
		while True:
			if self.stopped:
				return
			(self.grabbed, self.frame) = self.stream.read()


	def read(self):
		return (self.grabbed, self.frame)


	def stop(self):
		self.stopped = True
from imutils.video import VideoStream
import imutils
import cv2,os,urllib.request
import numpy as np
from django.conf import settings
import asyncio
from multiprocessing import shared_memory
from multiprocessing.managers import SharedMemoryManager

class ImageManager(SharedMemoryManager):
    pass

class VideoCamera(object):

	#usando a camera sem memoria compartilhada
	#def __init__(self):
		#self.video = cv2.VideoCapture(0)
	#def __del__(self):
		#self.video.release()
	
	#sem usar rede
	#def get_frame(self):
		#existing_shm = shared_memory.SharedMemory(name='uniquename')
		#image = np.ndarray((480,640,3), dtype=np.uint8, buffer=existing_shm.buf)
		#frame_flip = cv2.flip(image,1)
		#ret, jpeg = cv2.imencode('.jpg', frame_flip)
		#return jpeg.tobytes()

	#usando rede local
	def get_frame(self):
		ImageManager.register('getSharedMemory')
		smm = ImageManager(address=('127.0.0.1', 50000), authkey=b'abc')
		smm.connect()
		existing_shm = smm.getSharedMemory()
		image = existing_shm.copy()
		frame_flip = cv2.flip(image,1)
		ret, jpeg = cv2.imencode('.jpg', frame_flip)
		return jpeg.tobytes()
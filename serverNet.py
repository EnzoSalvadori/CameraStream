# In the first Python interactive shell
import time
import numpy as np
import cv2
from multiprocessing import shared_memory
from managers import SharedMemoryManager
from functools import partial

class ImageManager(SharedMemoryManager):
    pass

def getshm1(shm):
	img = np.ndarray((480,640,3), dtype=np.uint8, buffer=shm.buf)
	return img

if __name__ == '__main__':

	cap = cv2.VideoCapture(0)
	ret, img = cap.read()
	shm = shared_memory.SharedMemory(name='uniquename', create=True, size=img.nbytes)
	b = np.ndarray(img.shape, dtype=img.dtype, buffer=shm.buf)
	ImageManager.register('getSharedMemory', callable=partial(getshm1, shm))
	smm = ImageManager(address=('127.0.0.1', 50000), authkey=b'abc')
	smm.start()
	while(True):
		ret, img = cap.read()
		print(img.shape)
		print(img.dtype)
		b[:] = img[:]  # Copy the original data into shared memory
	# Clean up from within the first Python shell
	del b  # Unnecessary; merely emphasizing the array is no longer used
	shm.close()
	shm.unlink()  # Free and release the shared memory block at the very end
	print('server end')
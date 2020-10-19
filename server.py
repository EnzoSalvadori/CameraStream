# In the first Python interactive shell
import time
import numpy as np
import cv2
from multiprocessing import shared_memory
from functools import partial



cap = cv2.VideoCapture(0)
ret, img = cap.read()
shm = shared_memory.SharedMemory(name='uniquename', create=True, size=img.nbytes)
while(True):
	ret, img = cap.read()
	b = np.ndarray(img.shape, dtype=img.dtype, buffer=shm.buf)
	print(img.shape)
	print(img.dtype)
	b[:] = img[:]  # Copy the original data into shared memory
# Clean up from within the first Python shell
del b  # Unnecessary; merely emphasizing the array is no longer used
shm.close()
shm.unlink()  # Free and release the shared memory block at the very end
print('server end')
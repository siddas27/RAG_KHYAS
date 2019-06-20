import cv2
import numpy as np

from mjpeg_client import MJPEGClient

client = MJPEGClient('http://beaglebone.local:8080')

client.start()

for frame in client:

	if frame is None:
		sleep(1)
		continue

	buf = np.fromstring(frame, np.uint8)

	img = cv2.imdecode(buf, cv2.IMREAD_COLOR)

	cv2.imshow("test", img)
	cv2.waitKey(1)
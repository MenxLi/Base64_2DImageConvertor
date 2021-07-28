
"""An example for base64ImageConverter.py"""

import matplotlib.pyplot as plt
from b64ImConverter import imgEncodeB64, imgDecodeB64, batchImgEncodeB64, batchImgDecodeB64
import time

if __name__ == "__main__":
	im = plt.imread("test_img.jpg")
	print("Image size: ", im.shape)
	start_time = time.time()
	b64 = imgEncodeB64(im)
	print("Encoding time for a single image use imgEncodeB64: {}s".format(time.time() - start_time))

	start_time = time.time()
	im_rec = imgDecodeB64(b64)
	print("Decoding time for a single image use imgDecodeB64: {}s".format(time.time() - start_time))

	ims = [im]*100
	start_time = time.time()
	b64s = batchImgEncodeB64(ims)
	print("Encoding time (100 images) using batchImageEncodeB64: {}s".format(time.time() - start_time))

	start_time = time.time()
	ims_rec = batchImgDecodeB64(b64s)
	print("Decoding time (100 images) using batchImageDecodeB64: {}s".format(time.time() - start_time))

	plt.subplot(121)
	plt.imshow(im)
	plt.subplot(122)
	plt.imshow(im_rec)
	plt.show()

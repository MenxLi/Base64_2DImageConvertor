
"""An example for base64ImageConverter.py"""

import matplotlib.pyplot as plt
from base64ImageConverter import imgEncodeB64, imgDecodeB64
import time

im = plt.imread("test_img.jpg")
start_time = time.time()
b64 = imgEncodeB64(im, accelerate = True)
print("Encoding time: ", time.time() - start_time)

start_time = time.time()
im_rec = imgDecodeB64(b64, accelerate = True)
print("Decoding time: ", time.time() - start_time)

#  print("Encoded string: ", b64)

plt.subplot(121)
plt.imshow(im)
plt.subplot(122)
plt.imshow(im_rec)
plt.show()

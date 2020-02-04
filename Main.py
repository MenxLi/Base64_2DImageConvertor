
from base64ImageConverter import *

im = plt.imread("test_img.jpg")

encoder = Base64_2DImageEncoder(im, 8)
b64 = encoder.run()
decoder = Base64_2DImageDecoder(b64)
im_rec = decoder.run()

print(b64[:1000] + "...")

plt.subplot(121)
plt.imshow(im)
plt.subplot(122)
plt.imshow(im_rec)
plt.show()

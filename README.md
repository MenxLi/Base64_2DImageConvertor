# Base64_2DImageConvertor
Encode and decode between 2D image and Base64 string  
Module dependency: `numpy`  
The method is accelerated with `Ctypes`, to use pure python version, set `accelerate = False`  

For an example see `Main.py`:

```python
"""An example for base64ImageConverter.py"""

import matplotlib.pyplot as plt
from base64ImageConverter import imgEncodeB64, imgDecodeB64

im = plt.imread("test_img.jpg")
# start_time = time.time()
b64 = imgEncodeB64(im, accelerate = True)
# print("Encoding time: ", time.time() - start_time)

# start_time = time.time()
im_rec = imgDecodeB64(b64, accelerate = True)
# print("Decoding time: ", time.time() - start_time)

plt.subplot(121)
plt.imshow(im)
plt.subplot(122)
plt.imshow(im_rec)
plt.show()
```
    
Each pixel in the image will be converted into bits of minimum length to save the space.  
The encoded string has a header at the beginning to record those information.  
Thus the encoded string should be decoded only with this decoder, vise versa.

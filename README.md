# Base64_2DImageConvertor
Encode and decode between 2D image and Base64 string  
Module dependence: `numpy`

For an example see `Main.py`:

```
"""An example for base64ImageConverter.py"""

import matplotlib.pyplot as plt
from base64ImageConverter import imgEncodeB64, imgDecodeB64

im = plt.imread("test_img.jpg")
b64 = imgEncodeB64(im, 8)
im_rec = imgDecodeB64(b64)

print("Encoded string: ", b64[:1000] + "...")

plt.subplot(121)
plt.imshow(im)
plt.subplot(122)
plt.imshow(im_rec)
plt.show()
```
    

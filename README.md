# Base64_2DImageConvertor
Encode and decode between 2D image and Base64 string  
Module dependence: `numpy`

For an example see `Main.py`:

```python
"""An example for base64ImageConverter.py"""

import matplotlib.pyplot as plt
from base64ImageConverter import imgEncodeB64, imgDecodeB64

im = plt.imread("test_img.jpg")     # original image
b64 = imgEncodeB64(im, 8)           # ecoded string
im_rec = imgDecodeB64(b64)          # recovered image

```
    

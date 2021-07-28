# Base64_2DImageConvertor
Encode and decode between 2D image and Base64 string  
Module dependency: `numpy`  

For an example see `demo.py`:

```python
"""An example for b64ImConverter"""

import matplotlib.pyplot as plt
from b64ImConverter import imgEncodeB64, imgDecodeB64

im = plt.imread("test_img.jpg")
ims = [im]*100

start_time = time.time()
b64 = imgEncodeB64(im)
print("Encoding time for a single image use imgEncodeB64: {}s".format(time.time() - start_time))

start_time = time.time()
im_rec = imgDecodeB64(b64)
print("Decoding time for a single image use imgDecodeB64: {}s".format(time.time() - start_time))

start_time = time.time()
b64s = batchImgEncodeB64(ims)
print("Encoding time (100 images) using batchImageEncodeB64: {}s".format(time.time() - start_time))

start_time = time.time()
ims_rec = batchImgDecodeB64(b64s)
print("Decoding time (100 images) using batchImageDecodeB64: {}s".format(time.time() - start_time))

```
```bash
>> Image size:  (168, 210, 3)
Encoding time for a single image use imgEncodeB64: 0.08699989318847656s
Decoding time for a single image use imgDecodeB64: 0.00581669807434082s
Encoding time (100 images) using batchImageEncodeB64: 2.8371481895446777s
Decoding time (100 images) using batchImageDecodeB64: 0.22652578353881836s
```
    
Each pixel in the image will be converted into bits of minimum length to save the space.  
The encoded string has a header at the beginning to record those information.  
**Thus the encoded string should be decoded only with this decoder, vise versa.**

## Known issue
None. 
Please let me know any issue you found.
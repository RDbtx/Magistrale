"""
- LOCAL ADAPTIVE HISTOGRAM EQUALIZATION
Local Adaptive Histogram Equalization is a technique that enhances contrast locally by computing
histograms for small regions of an image using a moving window approach.

How It Works:
1. 2. 3. 4. Divide the image into small blocks (small rectangular region (or kernel) that slides across the image,
processing one small section at a time).

What to do:
Compute the histogram of pixel intensities for each block.
Apply histogram equalization within each block.
Use bilinear interpolation to smooth transitions between blocks.

Hints:
To perform this task OpenCV provides CLAHE (Contrast Limited Adaptive Histogram Equalization),
which does use tiles internally, but then interpolates between them to reduce block artifacts.

EXAMPLE:
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
eq_img = clahe.apply(gray_img)

scikit-image has exposure.equalize_adapthist(), same idea.

ATTENTION!
CLAHE only works on single channel images such as only grayscale images.
"""


import cv2
import numpy as np
from matplotlib import pyplot as plt

# Lets define the equalization function
def streach(im, nbr_bins=256):
    imhist, bins = np.histogram(im.flatten(), nbr_bins, [0, 256])
    cdf = imhist.cumsum()
    cdf = imhist.max() * cdf / cdf.max()
    cdf_mask = np.ma.masked_equal(cdf, 0)
    cdf_mask = (cdf_mask - cdf_mask.min()) * 255 / (cdf_mask.max() - cdf_mask.min())
    cdf = np.ma.filled(cdf_mask, 0).astype('uint8')
    return cdf[im.astype('uint8')]

bgr = cv2.imread(
    '/Volumes/SSD Esterna/Progetti/ComputerVision/Tutoring/Tutorato01/Dataset/Face.png'
)
gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
gray_hist = cv2.calcHist([gray], [0], None, [256], [0, 256])
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
clahe_img = clahe.apply(gray)
clahe_hist = cv2.calcHist([clahe_img], [0], None, [256], [0, 256])


# CLAHE function already does block separation, applies histogram equalization to each block
# and then reconstruct the new equalized image
fig, axes = plt.subplots(2, 2, figsize=(20, 6))
fig.suptitle('ORIGINAL VS EQUALIZED', color="blue", fontweight='bold', fontsize=15)

axes[0,0].imshow(gray, cmap='gray')
axes[0,0].axis('off')
axes[0,0].set_title("Original Image")

axes[1,0].imshow(clahe_img, cmap='gray')
axes[1,0].axis('off')
axes[1,0].set_title("Equalized Image")

axes[0,1].plot(gray_hist)
axes[0,1].set_xlim([0, 256])
axes[0,1].set_title('Original Histogram')
axes[0,1].grid(True)

axes[1,1].plot(clahe_hist)
axes[1,1].set_xlim([0, 256])
axes[1,1].set_title('Equalized Histogram')
axes[1,1].grid(True)

plt.show()
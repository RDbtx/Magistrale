"""
- LOCAL HISTOGRAM EQUALIZATION
Local Histogram Equalization is a localized version of histogram equalization that enhances contrast in small regions
(blocks) of an image rather than globally.

How It Works
1. 2. Divide the image into blocks (small non-overlapping regions).

What to do:
Equalize the histogram of each block independently.

ATTENTION!
This code only works for squared images.
"""

import cv2
import numpy as np
from matplotlib import pyplot as plt
from random import randrange

# Read image in BGR (default color order in OpenCV)
bgr = cv2.imread(
    '/Volumes/SSD Esterna/Progetti/ComputerVision/Tutoring/Tutorato01/Dataset/Face.png'
)

# Image properties
height, width, depth = bgr.shape
print(
    f"Image properties:\n"
    f"Image shape: {bgr.shape}\n"
    f"Width = {width} Height = {height} Depth = {depth}\n"
)

# Subdivide into blocks (small non-overlapping regions)
# Since the image Area is 182 * 182 lets use a 182 divisor =  1, 2, 7, 13, 14, 26, 91
blocks_per_side = 7
bh = height // blocks_per_side  # // to return integers
bw = width // blocks_per_side
print(
    f"Blocks per side: {blocks_per_side}\n"
    f"Block size: {blocks_per_side * blocks_per_side}\n"
    f"New Width: {bw} New Height: {bh}\n"
)
blocks = []
for i in range(blocks_per_side):
    for j in range(blocks_per_side):
        y0 = i * bh
        x0 = j * bw
        y1 = (i + 1) * bh
        x1 = (j + 1) * bw
        block = bgr[y0:y1, x0:x1]
        blocks.append(block)

# Preview chopped image (convert BGR->RGB for correct colors)
fig1, axes = plt.subplots(blocks_per_side, blocks_per_side, figsize=(20, 6))
fig1.suptitle(f'CHOPPED IMAGE {blocks_per_side}*{blocks_per_side}', color="blue", fontweight='bold', fontsize=15)

for i in range(blocks_per_side):
    for j in range(blocks_per_side):
        idx = i * blocks_per_side + j
        axes[i, j].imshow(cv2.cvtColor(blocks[idx], cv2.COLOR_BGR2RGB))
        axes[i, j].axis('off')
fig1.subplots_adjust(hspace=0.1)


# Contrast stretching function definition (EQUALIZATION)
def streach(im, nbr_bins=256):
    imhist, bins = np.histogram(im.flatten(), nbr_bins, [0, 256])
    cdf = imhist.cumsum()
    cdf = imhist.max() * cdf / cdf.max()
    cdf_mask = np.ma.masked_equal(cdf, 0)
    cdf_mask = (cdf_mask - cdf_mask.min()) * 255 / (cdf_mask.max() - cdf_mask.min())
    cdf = np.ma.filled(cdf_mask, 0).astype('uint8')
    return cdf[im.astype('uint8')]


fig2, axes = plt.subplots(blocks_per_side, blocks_per_side, figsize=(20, 6))
fig2.suptitle(f'EQUALIZED IMAGE -PER BLOCK- {blocks_per_side}*{blocks_per_side}', color="blue", fontweight='bold',
              fontsize=15)

eq_blocks = []
for i in range(blocks_per_side):
    for j in range(blocks_per_side):
        idx = i * blocks_per_side + j
        gray_blk = cv2.cvtColor(blocks[idx], cv2.COLOR_BGR2GRAY)
        eq_blk = streach(gray_blk)
        eq_blocks.append(eq_blk)
        axes[i, j].imshow(eq_blk, cmap='gray')
        axes[i, j].axis('off')
fig2.subplots_adjust(hspace=0.1)

# Now check histograms on one sample block taken at random
block_number = randrange(1, blocks_per_side * blocks_per_side)

gray_img = cv2.cvtColor(blocks[block_number], cv2.COLOR_BGR2GRAY)
eq_img = streach(gray_img)
hist = cv2.calcHist([gray_img], [0], None, [256], [0, 256])
eq_hist = cv2.calcHist([eq_img], [0], None, [256], [0, 256])

fig3, axes = plt.subplots(2, 2, figsize=(20, 6))
fig3.suptitle(f'BLOCK EQUALIZATION OF BLOCK {block_number}', color="blue", fontweight='bold', fontsize=15)

axes[0, 0].imshow(gray_img, cmap='gray')
axes[0, 0].set_title('Original block')
axes[0, 0].axis('off')

axes[1, 0].imshow(eq_img, cmap='gray')
axes[1, 0].set_title('Equalized block')
axes[1, 0].axis('off')

axes[0, 1].plot(hist)
axes[0, 1].set_xlim([0, 256])
axes[0, 1].set_title('Original histogram')
axes[0, 1].grid(True)

axes[1, 1].plot(eq_hist)
axes[1, 1].set_xlim([0, 256])
axes[1, 1].set_title('Equalized histogram')
axes[1, 1].grid(True)

# stitch back the locally equalized blocks (already grayscale)
rows_eq = []
for i in range(blocks_per_side):
    row = np.hstack(eq_blocks[i * blocks_per_side:(i + 1) * blocks_per_side])
    rows_eq.append(row)
eq_full = np.vstack(rows_eq)

# compute histogram of the reconstructed equalized image
eq_full_hist = cv2.calcHist([eq_full], [0], None, [256], [0, 256])

# now lets consider the original image
gray_bgr = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)
gray_bgr_hist = cv2.calcHist([gray_bgr], [0], None, [256], [0, 256])

# show reconstructed image + its histogram
fig4, ax4 = plt.subplots(2, 2, figsize=(8, 8))
fig4.suptitle('ORIGINAL VS EQUALIZED', color="blue",
              fontweight='bold', fontsize=15)

ax4[0,0].imshow(eq_full, cmap='gray')
ax4[0,0].axis('off')
ax4[0,0].set_title('Reconstructed equalized image')

ax4[0,1].plot(eq_full_hist)
ax4[0,1].set_xlim([0, 256])
ax4[0,1].set_title('Histogram of reconstructed image')
ax4[0,1].grid(True)

ax4[1,0].imshow(gray_bgr, cmap='gray')
ax4[1,0].axis('off')
ax4[1,0].set_title('Original grayscale image')

ax4[1,1].plot(gray_bgr_hist)
ax4[1,1].set_xlim([0, 256])
ax4[1,1].set_title('Histogram of original grayscale image')
ax4[1,1].grid(True)

plt.show()

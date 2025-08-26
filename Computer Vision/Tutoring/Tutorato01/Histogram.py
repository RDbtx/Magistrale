import cv2
import numpy as np
from matplotlib import pyplot as plt

# Read image in BGR (default color order in OpenCV)
bgr = cv2.imread(
    '/Volumes/SSD Esterna/Progetti/ComputerVision/Tutoring/Tutorato01/Dataset/Face.png'
)

# ---- First plot: raw BGR image vs RGB converted----

# Creates a figure with 1 row and 2 columns of subplots, wide size.
fig1, axes = plt.subplots(1, 2, figsize=(20, 6))
# Adds a main title for the figure.
fig1.suptitle('Raw BRG vs RGB converted', color='blue', fontweight="bold", fontsize=15)

# Left subplot: shows the original image as loaded by OpenCV in BGR order.
axes[0].imshow(bgr)
axes[0].set_title("Image extracted with CV2 in BGR")

# Convert to RGB (correct order for Matplotlib visualization).
rgb = cv2.cvtColor(bgr, cv2.COLOR_BGR2RGB)
(h, w, d) = bgr.shape

# Right subplot: shows the correctly converted RGB image.
axes[1].imshow(rgb)
axes[1].set_title('Image converted to RGB by Matplotlib')

# Add caption with image properties under the whole figure
props_text = (f"Properties:\n"
              f"Shape: {bgr.shape}\n"
              f"Total pixels: {bgr.size}\n"
              f"Width={w}, Height={h}, Depth={d}")
fig1.text(0.5, 0.01, props_text, ha="center", fontsize=10)

# ---- Second plot: Grayscaled image and its histogram---
# Creates a new figure with 1 row and 2 columns for grayscale and histogram.
fig2, axes = plt.subplots(1, 2, figsize=(20, 6))
fig2.suptitle('Grayscaled and its Histogram', color='blue', fontweight="bold", fontsize=15)

# Convert the image to grayscale.
gray = cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY)

# Left subplot: grayscale image.
axes[0].imshow(gray, cmap="gray")
axes[0].set_title('Grayscale image')

# Right subplot: histogram of grayscale intensities.
axes[1].hist(gray.ravel(), 256, range=[0, 256])
axes[1].set_title('Histogram of grayscale')
axes[1].grid(True)

# --- Third plot: BGR visualization in grayscale---
# Creates a new figure with 2 rows and 4 columns for B, G, R channels and histograms.
fig3, axes = plt.subplots(2, 4, figsize=(20, 8))
fig3.suptitle('BGR channel visualization', color='blue', fontweight="bold", fontsize=15)

# Split the BGR image into its three channels.
b, g, r = cv2.split(bgr)

# Blue channel: top-left image and bottom histogram.
axes[0, 0].imshow(b, cmap="gray")
axes[0, 0].set_title('Blue channel grayscaled image')
axes[1, 0].hist(b.ravel(), 256, range=[0, 256])
axes[1, 0].set_title('Histogram of grayscaled blue channel')
axes[1, 0].grid(True)

# Green channel: top image and bottom histogram.
axes[0, 1].imshow(g, cmap="gray")
axes[0, 1].set_title('Green channel grayscaled image')
axes[1, 1].hist(g.ravel(), 256, range=[0, 256])
axes[1, 1].set_title('Histogram of grayscaled green channel')
axes[1, 1].grid(True)

# Red channel: top image and bottom histogram.
axes[0, 2].imshow(r, cmap="gray")
axes[0, 2].set_title('Red channel grayscaled image')
axes[1, 2].hist(r.ravel(), 256, range=[0, 256])
axes[1, 2].set_title('Histogram of grayscaled red channel')
axes[1, 2].grid(True)

# Hide unused subplot (top-right empty).
axes[0, 3].axis('off')

# Combined BGR intensity histogram.
colors = ('b', 'g', 'r')
for i, col in enumerate(colors):
    histr = cv2.calcHist([bgr], [i], None, [256], [0, 256])
    axes[1, 3].plot(histr, color=col)
axes[1, 3].set_title("BGR intensity")
axes[1, 3].set_xlim([0, 256])
axes[1, 3].grid(True)

# --- Fourth plot: Image manipulation---
# Creates a new figure with 2 rows and 3 columns for segmentation, inversion, and contrast stretching.
fig3, axes = plt.subplots(2, 3, figsize=(20, 8))
fig3.suptitle('Image manipulation', color='blue', fontweight="bold", fontsize=15)

# Image segmentation using Otsu thresholding.
ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
axes[0, 0].imshow(thresh, cmap="gray")
axes[0, 0].set_title("Segmentation image")

# Grayscale inversion (inverting colors).
im2 = 255 - rgb
axes[0, 1].imshow(im2, cmap="gray")
axes[0, 1].set_title("Grayscale inverted image")


# Contrast stretching function definition.
def streach(im, nbr_bins=256):
    """ Contrast streaching of a grayscale image.  """
    # Compute the histogram of the image.
    imhist, bins = np.histogram(im.flatten(), nbr_bins, [0, 256])
    # Compute the cumulative distribution function (CDF).
    cdf = imhist.cumsum()
    # Normalize the CDF.
    cdf = imhist.max() * cdf / cdf.max()
    # Mask pixels with zero value.
    cdf_mask = np.ma.masked_equal(cdf, 0)
    # Apply linear stretching.
    cdf_mask = (cdf_mask - cdf_mask.min()) * 255 / (cdf_mask.max() - cdf_mask.min())
    # Fill masked values with zeros and cast to uint8.
    cdf = np.ma.filled(cdf_mask, 0).astype('uint8')
    # Map the image pixels using the new CDF.
    return cdf[im.astype('uint8')]


# Apply the contrast stretching function.
eq = streach(gray)
axes[0, 2].imshow(eq, cmap="gray")
axes[0, 2].set_title("Contrast streached image")

# Histogram before equalization.
axes[1, 0].hist(gray.ravel(), bins=256, range=[0, 256])
axes[1, 0].set_title("Histogram before equalization")
axes[1, 0].grid(True)

# Histogram after contrast stretching.
axes[1, 2].hist(eq.ravel(), bins=256, range=[0, 256])
axes[1, 2].set_title("Histogram after equalization")
axes[1, 2].grid(True)

# Hide middle empty subplot.
axes[1, 1].axis('off')

# Adjust layout and show all figures.
plt.tight_layout()
plt.show()

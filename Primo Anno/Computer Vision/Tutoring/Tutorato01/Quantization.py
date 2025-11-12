"""
2- QUANTIZATION
Image quantization is the process of converting the
continuous range of pixel values (intensities) into a
limited set of discrete values. This step follows sampling
and reduces the precision of the sampled values to a
manageable level for digital representation.

EXAMPLE:
"""
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread

pizza = imread('/Volumes/SSD Esterna/Progetti/ComputerVision/Tutoring/Tutorato01/Dataset/pizza.jpg')

factors = 2 ** np.arange(1, 5)

# Creates a row of subplots, one for each quantization factor.
# figsize=(20,6) makes it wide so the images fit side by side.

figure, axis = plt.subplots(1, len(factors), figsize=(20, 6))

# Iterates over each factor (k = 2, 4, 8, 16) and its subplot axis.

for k, ax in zip(factors, axis):

    # Creates k equally spaced thresholds between 0 and the maximum pixel value in the image.
    # Example: if pizza.max() = 255 and k=4, bins = [0, 85, 170, 255].

    bins = np.linspace(0, pizza.max(), k)

    # Assigns each pixel to a bin index depending on which range it falls into.
    # For instance, pixel value 100 would go to bin 2 if bins = [0, 85, 170, 255].

    image = np.digitize(pizza, bins)

    # Converts the bin index back into the actual bin representative value:
    # image - 1 shifts indices so they match Python’s 0-based indexing.
    # bins.tolist().__getitem__ returns the corresponding bin value.
    # np.vectorize(...) applies this to the whole array.
    # End result: every pixel is replaced with the nearest bin value (quantized intensity).

    image = (np.vectorize(bins.tolist().__getitem__)(image - 1).astype(int))

    # Displays the quantized image.
    # Title shows how many bins were used (k).

    ax.imshow(image)
    ax.set_title('$k = {}$'.format(k))
plt.show()

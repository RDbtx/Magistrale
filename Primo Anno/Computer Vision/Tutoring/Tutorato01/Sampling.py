"""
1- SAMPLING
Image sampling is the process of converting a continuous image (analog)
into a discrete image (digital) by selecting specific
points from the continuous image. Increasing the number N of
pixels in the image, we can better represent an analog
object into a digital image.

EXAMPLE:
"""
import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread


    # Loads the image "pizza.jpg" into a NumPy array called pizza.
    # Each pixel is represented as an array of RGB values

pizza = imread('/Volumes/SSD Esterna/Progetti/ComputerVision/Tutoring/Tutorato01/Dataset/pizza.jpg')

    # Imports the function downscale_local_mean from scikit-image.
    # This function reduces the resolution of an image by taking the local mean of pixel blocks instead of
    # just skipping pixels (which keeps the image visually smoother).

from skimage.transform import downscale_local_mean

    # Creates an array of downscaling factors:
    # np.arange(1,5) → [1, 2, 3, 4]
    # 3**[...] → [3, 9, 27, 81]
    # So we will downscale the image by factors of 3, 9, 27, and 81.

factors = 3 ** np.arange(1, 5)

    # Creates a matplotlib figure with 1 row and len(factors) = 4 columns of subplots.
    # axis will be a NumPy array of 4 subplot axes objects.
    # figsize=(20,6) makes the figure large and wide.

figure, axis = plt.subplots(1, len(factors), figsize=(20, 6))

    # Iterates over each factor and corresponding subplot axis.
    # downscale_local_mean(pizza, factors=(factor, factor, 1)) downsamples the image:
    # (factor, factor, 1) means reduce resolution in both height and width by factor,
    # but not in the color channel (1).
    # .astype(int) converts the resulting float array to integers (pixel values).
    # Displays the downscaled image in the subplot with ax.imshow(image).
    # Adds a title showing the new number of rows (height) of the image:
    # Example: if the original image was 600x800, after factor=3, the new height would be 200.

for factor, ax in zip(factors, axis):
    image = downscale_local_mean(pizza, factors=(factor, factor, 1)).astype(int)
    ax.imshow(image)
    ax.set_title('$N={}$'.format(image.shape[0]))

    # Displays the entire figure with the four images side by side.

plt.show()


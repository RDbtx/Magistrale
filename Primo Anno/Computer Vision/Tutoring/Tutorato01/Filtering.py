import cv2
import numpy as np
import matplotlib.pyplot as plt

def show_images(suptitle, image_list, title_list, rows=1, cols=3, cmap=None):
    """Function to display multiple images dynamically with titles"""
    plt.figure(figsize=(15, 5))
    plt.suptitle(suptitle, fontsize=15, fontweight='bold')
    for i, (img, title) in enumerate(zip(image_list, title_list)):
        plt.subplot(rows, cols, i+1)
        plt.imshow(img, cmap=cmap)
        plt.title(title)
        plt.axis("off")  # Hide axis
    plt.show()



# --- MANUAL FILTERING ---
def wrappingImage(img, kernelSize: int):
    """
    Extend the image boundaries using wrapping (mirroring) to handle kernel operations.
    This prevents border artifacts when applying mean or median filters.
    """
    w = kernelSize // 2  # Width of the padding (half the kernel size)

    # Fetch first and last rows for wrapping (mirror effect)
    fetchFirstRows = img[0:w, :]
    fetchLastRows = img[-w:, :]

    imgWrapped = img.copy()
    imgWrapped = np.insert(imgWrapped, 0, fetchLastRows, axis=0)
    imgWrapped = np.append(imgWrapped, fetchFirstRows, axis=0)

    # Fetch first and last columns for wrapping
    fetchFirstCols = imgWrapped[:, 0:w]
    fetchLastCols = imgWrapped[:, -w:]

    imgWrapped = np.concatenate((fetchLastCols, imgWrapped), axis=1)
    imgWrapped = np.append(imgWrapped, fetchFirstCols, axis=1)

    return imgWrapped


def meanFilter(originalImg, wrappedImage, kernelSize: int):
    """
    Applies a Mean Filter to remove noise by averaging pixel values within a kernel.
    """
    filteredImage = np.zeros(originalImg.shape, dtype=np.int32)
    image_h, image_w = originalImg.shape[0], originalImg.shape[1]
    w = kernelSize // 2  # Half-size of the kernel

    # Traverse through the image
    for i in range(w, image_h - w):
        for j in range(w, image_w - w):
            total = [0, 0, 0]  # Store RGB sum

            # Apply kernel window
            for m in range(kernelSize):
                for n in range(kernelSize):
                    total += wrappedImage[i - w + m][j - w + n]  # Sum values in the kernel

            # Compute the mean
            filteredImage[i - w][j - w] = total // (kernelSize * kernelSize)

    return filteredImage


def medianFilter(originalImg, wrappedImage, kernelSize: int):
    """
    Applies a Median Filter to reduce noise by replacing each pixel with the median of its neighborhood.
    """
    filteredImage = np.zeros(originalImg.shape, dtype=np.int32)
    image_h, image_w = originalImg.shape[0], originalImg.shape[1]
    w = kernelSize // 2

    # Traverse the image
    for i in range(w, image_h - w):
        for j in range(w, image_w - w):
            # Extract the kernel region
            overlapImg = wrappedImage[i - w:i + w + 1, j - w:j + w + 1]  # Crop the area

            # Compute the median for each channel (RGB)
            filteredImage[i][j] = np.median(overlapImg.reshape(-1, 3), axis=0)

    return filteredImage

# Reading the image
image_path = "/Volumes/SSD Esterna/Progetti/ComputerVision/Tutoring/Tutorato01/Dataset/fingerprint.jpg"
image_bgr = cv2.imread(image_path)
image_rgb = cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)

kernel_size = 5  # TRY WITH DIFFERENT KERNEL SIZES ##
wrapped_img = wrappingImage(image_rgb, kernel_size) # Apply image wrapping
mean_filtered = meanFilter(image_rgb, wrapped_img, kernel_size) # Apply Mean Filter
median_filtered = medianFilter(image_rgb, wrapped_img, kernel_size) # Apply Median Filter

show_images(
    "Manual Filtering",
    [image_rgb, wrapped_img, mean_filtered, median_filtered],
    ["Original (RGB)", "Wrapped Image", "Mean Filter", "Median Filter"],
    rows=1, cols=4
)


# --- FILTERING WITH OPENCV ---

image_mean = cv2.GaussianBlur(image_rgb, (5, 5), 0) # Apply Mean filter
image_median = cv2.medianBlur(image_rgb, 5) # Apply Median filter

show_images(
    "Filtering with OPEN CV",
    [image_rgb, image_mean, image_median],
    ["Original (RGB)", "Mean Blur", "Median Filter"]
)


# --- FILTERING WITH KERNELS ---

# Define sharpening kernels
kernel_laplacian = np.array([[0, 1, 0], ## YOUR CODE HERE ##
                             [1, -4, 1],
                             [0, 1, 0]])

kernel_sobel_x = np.array([[-1, 0, 1], ## YOUR CODE HERE ##
                           [-2, 0, 2],
                           [-1, 0, 1]])

kernel_sobel_y = np.array([[-1, -2, -1], ## YOUR CODE HERE ##
                           [0,  0,  0],
                           [1,  2,  1]])

kernel_emboss = np.array([[-2, -1, 0], ## YOUR CODE HERE ##
                          [-1,  1, 1],
                          [ 0,  1, 2]])

# Apply kernels to the original image
image_Laplacian = cv2.filter2D(image_rgb, -1, kernel_laplacian)## YOUR CODE HERE ##
image_Sobel_X = cv2.filter2D(image_rgb, -1, kernel_sobel_x) ## YOUR CODE HERE ##
image_Sobel_Y = cv2.filter2D(image_rgb, -1, kernel_sobel_y) ## YOUR CODE HERE ##
image_Emboss = cv2.filter2D(image_rgb, -1, kernel_emboss) ## YOUR CODE HERE ##


# Display the images
show_images(
    "Kernel Filtering",
    [image_rgb, image_Laplacian, image_Sobel_X, image_Sobel_Y, image_Emboss],
    ["Original (RGB)", "Laplacian", "Sobel X", "Sobel Y", "Emboss"],
    rows=1, cols=5
)

# --- IMAGE SMOOTHING AND SHARPENING USING FREQUENCY FILTERING ---


image_gray = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
# Compute the Discrete Fourier Transform (DFT)
dft = np.fft.fft2(image_gray)  ## YOUR CODE HERE ##

# Shift the zero frequency component to the center
dft_shift = np.fft.fftshift(dft) ## YOUR CODE HERE ##

# Get the amplitude & Phase Spectrum
# Magnitude of the transformation
amplitude = np.abs(dft_shift) ## YOUR CODE HERE ##
# Phase of the transformation
phase = np.angle(dft_shift) ## YOUR CODE HERE ##

# Apply log to improve the amplitude visualization
# log(1 + amplitude) to normalize
amplitude_log = np.log1p(amplitude) ## YOUR CODE HERE ##

# Display the images
show_images(
    "Amplitude and Phase with Fourier Transform",
    [image_gray, amplitude_log, phase],
    ["Original (Gray)", "Amplitude Spectrum", "Phase Spectrum"],
    rows=1, cols=3,
    cmap='gray'
)


# Get image dimensions
rows, cols = image_gray.shape ## YOUR CODE HERE ##
# Center coordinates
crow, ccol = rows // 2, cols // 2 # YOUR CODE HERE ##

# Create a Low-Pass Filter (LPF)
radius = 30  # Change the radius to control the effect
low_pass = np.zeros((rows, cols), np.uint8) ## YOUR CODE HERE ##
# Circular LPF
cv2.circle(low_pass, (ccol, crow), radius, 1, -1) ## YOUR CODE HERE ##

# Create a High-Pass Filter (HPF)
high_pass = np.ones((rows, cols), np.uint8)
# Circular HPF
cv2.circle(high_pass, (ccol, crow), radius, 0, -1) # YOUR CODE HERE ##

# Apply filters in the frequency domain
dft_low = dft_shift * low_pass ## YOUR CODE HERE ##
dft_high = dft_shift * high_pass ## YOUR CODE HERE ##

# Inverse Fourier Transform to get back the spatial domain images
image_low = np.fft.ifft2(np.fft.ifftshift(dft_low)).real ## YOUR CODE HERE ##
image_high = np.fft.ifft2(np.fft.ifftshift(dft_high)).real # YOUR CODE HERE #


# Display the images
show_images(
    "Low Pass and High Pass Filtering",
    [image_gray, image_low, image_high],
    ["Original (Gray)", "Low-Pass Filtered Image (Blurred)", "High-Pass Filtered Image (Enhanced Edges)"],
    rows=1, cols=3,
    cmap='gray'
)


# --- EDGE DETECTION IN FINGERPRINTS ---
# Define a kernel for morphological operations (structural element)
kernel = np.ones((3, 3), np.uint8) # basic rectangular kernel (uniform effect)

# Apply Dilatation first
dilated = cv2.dilate(image_gray, kernel, iterations=1) ## YOUR CODE HERE ##

# Then apply erosion
eroded = cv2.erode(image_gray, kernel, iterations=1) ## YOUR CODE HERE ##

# Final do the subtraction operation
morph_gradient = dilated - eroded ## YOUR CODE HERE ##

# Apply Canny Edge Detection
canny_edges = cv2.Canny(image_gray, 50, 150) ## YOUR CODE HERE

# Display the images
print('OUTPUT:')
show_images(
    "Edge Detection",
    [image_gray, morph_gradient, canny_edges],
    ["Original (Gray)", "Morphological Gradient", "Canny Edge Detection"],
    rows=1, cols=3,
    cmap='gray'
)
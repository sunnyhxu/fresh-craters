import cv2
import numpy as np
import matplotlib.pyplot as plt


def calculate_glcm(image, distance=5, angle=0, levels=256):
    rows, cols = image.shape
    glcm = np.zeros((levels, levels), dtype=np.uint32)
    if angle == 0:
        for i in range(rows):
            for j in range(cols - distance):
                row = image[i, j]
                col = image[i, j + distance]
                glcm[row, col] += 1
    elif angle == 90:
        for i in range(rows - distance):
            for j in range(cols):
                row = image[i, j]
                col = image[i + distance, j]
                glcm[row, col] += 1

    glcm = glcm / glcm.sum()
    return glcm


def calculate_contrast(glcm):
    rows, cols = glcm.shape
    contrast = 0
    for i in range(rows):
        for j in range(cols):
            contrast += (i - j) ** 2 * glcm[i, j]
    return contrast


def calculate_homogeneity(glcm):
    rows, cols = glcm.shape
    homogeneity = 0
    for i in range(rows):
        for j in range(cols):
            homogeneity += glcm[i, j] / (1 + (i - j) ** 2)
    return homogeneity


image_path = "crater.png"
img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

blurred = cv2.GaussianBlur(img, (5, 5), 0)
edges = cv2.Canny(blurred, 50, 150)

contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
largest_contour = max(contours, key=cv2.contourArea)

area = cv2.contourArea(largest_contour)
perimeter = cv2.arcLength(largest_contour, True)
circularity = (4 * np.pi * area) / (perimeter ** 2) if perimeter > 0 else 0

glcm = calculate_glcm(img)
contrast = calculate_contrast(glcm)
homogeneity = calculate_homogeneity(glcm)

if circularity > 0.75 and homogeneity > 0.4:
    classification = "Bowl"
elif contrast > 50 and circularity < 0.6:
    classification = "Concentric"
else:
    classification = "Flat-floored"

plt.figure(figsize=(10, 5))
plt.subplot(1, 2, 1)
plt.imshow(img, cmap='gray')
plt.title("Original Image")

plt.subplot(1, 2, 2)
plt.imshow(edges, cmap='gray')
plt.title(f"Crater Classification: {classification}")

plt.show()
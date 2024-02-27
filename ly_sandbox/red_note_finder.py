import cv2
import numpy as np
from time import time

now = time()
# Load the image
image = cv2.imread('/Users/davidmay/Desktop/Code testing/notes.jpeg')

# Convert image to HSV color space
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Define range of red color in HSV
lower_red = np.array([0, 100, 100])
upper_red = np.array([10, 255, 255])

# Threshold the HSV image to get only red colors
mask = cv2.inRange(hsv, lower_red, upper_red)

# Find contours
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Get the largest contour
largest_contour = max(contours, key=cv2.contourArea)

# Get the centroid of the contour
M = cv2.moments(largest_contour)
cx = int(M['m10'] / M['m00'])
cy = int(M['m01'] / M['m00'])

# Print the centroid coordinates
print("Centroid coordinates (x, y):", cx, cy)
print("Time:", time()-now)

# Optionally, visualize the centroid
cv2.circle(image, (cx, cy), 5, (0, 255, 0), -1)  # Draw a green circle at the centroid
cv2.imshow('Image with centroid', image)
cv2.waitKey(0)
cv2.destroyAllWindows()

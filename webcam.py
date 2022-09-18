import numpy
import cv2

img = cv2.imread("images/sample3.png")

# 2. Resize the image
img = cv2.resize(img, None, fx=0.5, fy=0.5)

# 3. Convert image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# 4. Convert image to black and white (using adaptive threshold)
adaptive_threshold = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 85, 11)
text = pytesseract.image_to_string(img)
print(text)

cv2.imshow("gray", gray)
cv2.imshow("adaptive th", adaptive_threshold)
cv2.waitKey(0)
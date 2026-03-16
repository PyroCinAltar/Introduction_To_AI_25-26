import cv2
import matplotlib.pyplot as plt

image = cv2.imread("share.png", 0)
edges = cv2.Canny(image, 100, 200)
plt.imshow(edges, cmap='gray')
plt.axis("off")
plt.show()
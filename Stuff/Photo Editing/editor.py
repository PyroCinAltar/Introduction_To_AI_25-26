import cv2

image = cv2.imread("glec_chair.jpeg")

if image is None:
    print("Error: Image 'noisy_image.jpg' could not be loaded. Please ensure the file exists and the path is correct.")
else:
    denoised = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
    cv2.imwrite("clean_image.jpg", denoised)
    print("Image denoising complete. 'clean_image.jpg' saved.")
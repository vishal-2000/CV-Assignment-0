import cv2
import numpy as np

img = cv2.imread('./test_image.jpeg')
# print(img)

color_limits = [120, 190]
main_img = cv2.imread('./test_image_main.jpeg')
main_img.shape

alpha_channel = np.ones(shape=(1599, 899, 3))

# Masking
for i in range(1599):
    for j in range(899):
        if (main_img[i, j, 0] in range(color_limits[0], color_limits[1])) and (main_img[i, j, 1] in range(color_limits[0], color_limits[1])) and (main_img[i, j, 2] in range(color_limits[0], color_limits[1])):
            alpha_channel[i, j, 0] = 0
            alpha_channel[i, j, 1] = 0
            alpha_channel[i, j, 2] = 0
            
# print(alpha_channel)
# print(main_img)

print(main_img)

bg_img = cv2.imread('./test_bg2.jpeg')

bg_img = cv2.resize(bg_img, ( 899, 1599))

new_img = np.multiply(main_img, alpha_channel) + np.multiply(bg_img, (1-alpha_channel))

new_img = new_img.astype(np.uint8)

print(new_img)

print(main_img.shape)
print(new_img.shape)

# for i in range(1599):
#     for j in range(899):
#         for k in range(3):
#             if new_img[i, j, k] > 255:
#                 new_img[i, j, k] = 255
#                 print(255)
#             elif new_img[i, j, k] < 0:
#                 new_img[i, j, k] = 0
#                 print(0)

print("Yo!")
cv2.imshow('Modified', new_img)
cv2.waitKey(0)
cv2.imshow("The original", main_img)
cv2.waitKey(0)
print("Yo!")


# from video_to_image import Video
# import cv2
# import numpy as np

# vid = Video(video_file_path='./CV_test_vid.mp4')
# img_array = vid.convert_to_images_and_return()

# for img in img_array:
#     print("Image type: {}".format(type(img)))
#     cv2.imshow("The Original", img)
#     print(np.count_nonzero(img))
#     exit(1)
    

# for img in img_array:
#     print(img.shape)
    
import cv2
import numpy as np
from video_to_image import Video
from images_to_video import Images

fg_video_file_path = './T-Rex-foreground.mp4'
bg_video_file_path = './Background_vid.mp4'

fg_video = Video(video_file_path=fg_video_file_path)
fg_img_array = fg_video.convert_to_images_and_return()

bg_video = Video(video_file_path = bg_video_file_path)
bg_img_array = bg_video.convert_to_images_and_return()

color_limits = [[0, 1], [204, 208], [0, 2]]

img_res_array = []

# counter = 0
for f_img, b_img in zip(fg_img_array, bg_img_array):
    alpha_channel = np.ones(shape=(f_img.shape[0], f_img.shape[1], 3))
    b_img = cv2.resize(b_img, ( f_img.shape[1], f_img.shape[0]))
    # Masking element wise (extremely slow)
    # for i in range(f_img.shape[0]):
    #     for j in range(f_img.shape[1]):
    #         if (f_img[i, j, 0] in range(color_limits[0][0], color_limits[0][1])) and (f_img[i, j, 1] in range(color_limits[1][0], color_limits[1][1])) and (f_img[i, j, 2] in range(color_limits[2][0], color_limits[2][1])):
    #             alpha_channel[i, j, 0] = 0
    #             alpha_channel[i, j, 1] = 0
    #             alpha_channel[i, j, 2] = 0

    # Masking (Vectorized)
    red_ch_mask = np.logical_and(f_img[:, :, 0] >= 0, f_img[:, :, 0] <= 1)
    green_ch_mask = np.logical_and(f_img[:, :, 1] >= 204, f_img[:, :, 1] <= 208)
    blue_ch_mask = np.logical_and(f_img[:, :, 2] >= 0, f_img[:, :, 2] <= 2)

    for i in range(3):
        alpha_channel[:, :, i] = np.logical_not(np.logical_and(np.logical_and(red_ch_mask, green_ch_mask), blue_ch_mask))

    # alpha_channel[:, :, 0] = np.logical_and(np.logical_and(f_img[:, :, 0] >= 0, f_img[:, :, 0] <= 1), 
    # alpha_channel[:, :, 1] = np.logical_and(f_img >= 204, f_img <= 208)
    # alpha_channel[:, :, 0] = np.logical_and(f_img >= 0, f_img <= 1)

    # Add background image to the alpha multiplied foreground
    img_res = np.multiply(f_img, alpha_channel) + np.multiply(b_img, (1 - alpha_channel))

    img_res = img_res.astype(np.uint8)
    img_res_array.append(img_res)

    # counter += 1
    # if counter == 5:
    #     break

image_class = Images(image_dir_path = None)
image_class.convert_array_to_video_and_save(img_res_array, video_file_path='./result_fps=20.mp4', fps=20)



# img = cv2.imread('./test_image.jpeg')
# # print(img)

# color_limits = [120, 190]
# main_img = cv2.imread('./test_image_main.jpeg')
# main_img.shape

# alpha_channel = np.ones(shape=(1599, 899, 3))

# # Masking
# for i in range(1599):
#     for j in range(899):
#         if (main_img[i, j, 0] in range(color_limits[0], color_limits[1])) and (main_img[i, j, 1] in range(color_limits[0], color_limits[1])) and (main_img[i, j, 2] in range(color_limits[0], color_limits[1])):
#             alpha_channel[i, j, 0] = 0
#             alpha_channel[i, j, 1] = 0
#             alpha_channel[i, j, 2] = 0
            
# # print(alpha_channel)
# # print(main_img)

# print(main_img)

# bg_img = cv2.imread('./test_bg2.jpeg')

# bg_img = cv2.resize(bg_img, ( 899, 1599))

# new_img = np.multiply(main_img, alpha_channel) + np.multiply(bg_img, (1-alpha_channel))

# new_img = new_img.astype(np.uint8)

# print(new_img)

# print(main_img.shape)
# print(new_img.shape)

# print("Yo!")
# cv2.imshow('Modified', new_img)
# cv2.waitKey(0)
# cv2.imshow("The original", main_img)
# cv2.waitKey(0)
# print("Yo!")
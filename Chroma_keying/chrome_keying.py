from video_to_image import Video

vid = Video(video_file_path='./CV_test_vid.mp4')
img_array = vid.convert_to_images_and_return()

for img in img_array:
    print(img.shape)
    
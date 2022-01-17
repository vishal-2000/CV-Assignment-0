import cv2
import numpy as np
import copy
from video_to_image import Video
from images_to_video import Images
import matplotlib.pyplot as plt

def chi_squared_distance(arr1: np.ndarray, arr2: np.ndarray):
    '''
    Calculates the vectorized chi_squared distance between the two 1 dimensional numpy arrays
    
    Parameters:
    arr1: np.ndarray (1 dimensional)
    arr2: np.ndarray (1 dimensional)

    Return:
    distance: float
    '''

    diff = arr1 - arr2
    diff_sq = diff**2
    addition = arr1 + arr2
    resultant = diff_sq[addition!=0] / addition[addition!=0] # Only consider non-zero denominator elements (as zero elements don't effect the cost but can cause an exception (division by 0))
    return np.sum(resultant)


if __name__=='__main__':
    video = Video('./Peter_parker_dance.mp4')
    img_arr = video.convert_to_images_and_return()
    num_images = len(img_arr)
    # Adjacent frame differences
    adj_dists = []
    shot_ranges = []
    prev_i = 0
    for i in range(num_images - 1):
        ch1 = cv2.calcHist(images = [img_arr[i]], channels=[0, 1, 2], mask=None, histSize=[10, 10, 10], ranges=[0, 256, 0, 256, 0, 256])
        ch2 = cv2.calcHist(images = [img_arr[i+1]], channels=[0, 1, 2], mask=None, histSize=[10, 10, 10], ranges=[0, 256, 0, 256, 0, 256])
        adj_dists.append(chi_squared_distance(ch1.flatten(), ch2.flatten()))
        if adj_dists[-1] >= 1e5: # 5*(1e4):
            shot_ranges.append([prev_i, i])
            prev_i = i + 1
        #     cv2.imshow('current', img_arr[i])
        #     cv2.waitKey(1)
        #     cv2.imshow('next', img_arr[i+1])
        #     cv2.waitKey(0)

    print("No of shots: {}".format(len(shot_ranges)))
    image_cl = Images(image_dir_path='./trash')
    for i, shot in enumerate(shot_ranges):
        image_cl.convert_array_to_video_and_save(image_array=img_arr[shot[0]:shot[1]+1], video_file_path='./shots/shot_{}.mp4'.format(i), fps=24)

    cv2.destroyAllWindows()
    plt.plot(adj_dists)
    plt.show()
    # img = cv2.imread('./test_image_main.jpeg')
    # c_hist = cv2.calcHist(images = [img], channels=[0, 1, 2], mask=None, histSize=[10, 10, 10], ranges=[0, 256, 0, 256, 0, 256])
    # c2_hist = copy.deepcopy(c_hist)
    # print("Chi squared distance: {}".format(chi_squared_distance(c_hist.flatten(), c2_hist.flatten())))
    
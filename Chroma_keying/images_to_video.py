import cv2
import sys
import argparse
from os import listdir
from os.path import isfile, join
import os
import copy
import numpy as np

class Images:
    def __init__(self, image_dir_path: str) -> None:
        self.image_dir_path = image_dir_path

    def extract_frame_num_from_file_name(self, file_name: str) -> int:
        '''
        Given a file name of form <frame_num>_img.mp4, this function extracts the frame_num and
        returns it
        '''
        num_str = ''
        for i in file_name:
            if i == '_':
                break
            num_str += i
        return int(num_str)

    def convert_array_to_video_and_save(self, image_array: np.ndarray, video_file_path: str, fps: int):
        height, width, layers = image_array[0].shape
        size = (width,height)
        print("Video file creation in process")
        vid_writer = cv2.VideoWriter(video_file_path, cv2.VideoWriter_fourcc(*'mp4v'), fps=int(fps), frameSize=size)
        print("Video file created and written!")
        for i in image_array:
            print(i)
            vid_writer.write(i)
        vid_writer.release()

    def convert_to_video_and_save(self, video_file_path: str, fps: int):
        img_dir_path = self.image_dir_path
        if img_dir_path[-1] != '/':
            # print(img_dir_path+'/')
            img_dir_path = img_dir_path + '/'
            # print(img_dir_path)

        # Creating a dictionary with frame numbers as keys, file names as values
        image_files = [f for f in listdir(img_dir_path) if isfile(join(img_dir_path, f))]

        # image_file_dict is of form:
        #   image_file_dict = {
        #       <frame_num>: <file_name>
        #   }
        image_file_dict = {} 
        for file_name in image_files:
            frame_num = self.extract_frame_num_from_file_name(file_name)
            image_file_dict[str(frame_num)] = file_name
        
        # Extracting images from files and appending them to video file
        img_array = []
        for i in range(len(image_file_dict)):
            # print(img_dir_path +image_file_dict[str(i)])
            img = cv2.imread(img_dir_path + image_file_dict[str(i)])
            # print(img!=None)

            height, width, layers = img.shape
            size = (width,height)
            img_array.append(img)

        print("Video file creation in process")
        vid_writer = cv2.VideoWriter(video_file_path, cv2.VideoWriter_fourcc(*'mp4v'), fps=int(fps), frameSize=size)
        print("Video file created and written!")
        for i in img_array:
            vid_writer.write(i)
        vid_writer.release()

    # def convert_to_images_and_save(self, image_dir_path: str):
    #     if image_dir_path[-1] != '/':
    #         image_dir_path += '/'
    #     counter = 0
    #     while(self.video.isOpened()):
    #         ret, frame = self.video.read()
    #         if ret == False:
    #             print("Video stream ended! (or probably an error?)")
    #             break
            
    #         cv2.imwrite(image_dir_path+'img{}.jpg'.format(counter), frame)
    #         counter += 1

    #     self.video.release()
    #     self.video = cv2.VideoCapture(video_file_path)

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Video to Image options')
    parser.add_argument('-i', '--image_dir_path', help='Specify the absolute path to the directory where the images are to be stored', default='./Images') # required=True
    parser.add_argument('-v', '--video_path', help='Specify the absolute path to the video file that is to be converted to images', default='./Generated_videos/generated.mp4')
    parser.add_argument('-f', '--fps', help='Specify the frame rate for the generated video', default=20)
    args = vars(parser.parse_args())
    print(args)

    # Extracting parameters
    video_file_path = args['video_path']
    image_dir_path = args['image_dir_path']
    fps = args['fps']

    # Convert images to a video file and save it
    image_group = Images(image_dir_path)
    image_group.convert_to_video_and_save(video_file_path, fps)
    exit(0)
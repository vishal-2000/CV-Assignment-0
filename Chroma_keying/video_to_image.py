import cv2
import sys
import argparse

class Video:
    def __init__(self, video_file_path: str) -> None:
        self.video_file_path = video_file_path
        self.video = None
        # self.video = cv2.VideoCapture(video_file_path)

    def convert_to_images_and_save(self, image_dir_path: str):
        self.video = cv2.VideoCapture(self.video_file_path)
        if image_dir_path[-1] != '/':
            image_dir_path += '/'
        counter = 0
        while(self.video.isOpened()):
            ret, frame = self.video.read()
            if ret == False:
                print("Video stream ended! (or probably an error?)")
                break
            
            cv2.imwrite(image_dir_path+'{}_img.jpg'.format(counter), frame)
            counter += 1

        self.video.release()
        self.video = None
        # self.video = cv2.VideoCapture(video_file_path)

    def convert_to_images_and_return(self):
        self.video = cv2.VideoCapture(self.video_file_path)
        counter = 0
        img_array = []
        while(self.video.isOpened()):
            ret, frame = self.video.read()
            if ret == False:
                print("Video stream ended! (or probably an error?)")
                break
            
            img_array.append(frame)
            counter += 1

        self.video.release()
        self.video = None
        # self.video = cv2.VideoCapture(video_file_path)
        # print(self.video)
        return img_array

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Video to Image options')
    parser.add_argument('-v', '--video_path', help='Specify the absolute path to the video file that is to be converted to images', required=True)
    parser.add_argument('-i', '--image_dir_path', help='Specify the absolute path to the directory where the images are to be stored', required=True)
    args = vars(parser.parse_args())
    print(args)

    # Extracting parameters
    video_file_path = args['video_path']
    image_dir_path = args['image_dir_path']

    # Save frames as images and exit
    video = Video(video_file_path)
    video.convert_to_images_and_save(image_dir_path)

    exit()

    # Load and read video using openCV
    video = cv2.VideoCapture(video_file_path)

    if video.isOpened() == False:
        print("Error opening the video file, please check the file or path given")
    
    count = 8
    step = 3
    i = 0
    while(video.isOpened()):
        ret, frame = video.read()

        if ret == False: # Frame read incorrectly or video file ended
            print("Video stream ended! (or probably an error?)")
            break

        # gray = cv2.cvtColor(frame, )
        cv2.imshow('frame', frame)
        # print(count)
        if cv2.waitKey(count) == ord('q'):
            break
        i += 1
        if i%3==0:
            if count >= 70 or count <= 5:
                step = -1*step
            count += step


    video.release()
    cv2.destroyAllWindows()




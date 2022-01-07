# import the opencv library
import cv2
from datetime import datetime
import argparse

class Camera_capture:
    def __init__(self, camera_num = 0, image_dir_path = './Captured_images/') -> None:
        '''
        Parameters:
        camera_num - Each camera is assigned an integer number on your device. By default, if your
                    laptop has a webcam in-built, it takes '0' value. Other external cameras connected
                    will take values 1, 2, ...etc. If there is no webcam in-built, then the values for 
                    external cameras start from 0.
        '''
        self.camera_num = camera_num
        self.image_dir_path = image_dir_path
        if self.image_dir_path[-1] != '/':
            self.image_dir_path += '/'

    def start_cam(self):
        vid = cv2.VideoCapture(self.camera_num)
        print("\nCamera {} started!\n".format(self.camera_num))
        print("Instructions:")
        print("1. To capture an image, press 'c' key on your keyboard")
        print("2. To close the webcam and exit program, press 'q' key on your keyboard")
        print("3. Captured images will be stored in {} directory, if that directory exists".format(self.image_dir_path))
        print("4. Image naming convention: img_<year>_<month>_<day>_<hours>_<mins>_<secs>.jpg\n")

        while(True):
            # Capture the video frame by frame
            ret, frame = vid.read()
        
            # Display the resulting frame
            cv2.imshow('frame', frame)
            
            # Press q to exit, c to capture an image
            wait_key = cv2.waitKey(1)

            if wait_key == ord('q'): # To quit the webcam capture
                print("Closed cam")
                break
            elif wait_key == ord('c'): # To capture and save current image frame from webcam stream
                current_time = datetime.now()
                current_time_formatted = current_time.strftime("%Y_%m_%d_%H_%M_%S")
                cv2.imwrite('{}img_{}.jpg'.format(self.image_dir_path, current_time_formatted), frame)
                print("Captured")

        # After the loop release the cap object
        vid.release()
        # Destroy all the windows
        cv2.destroyAllWindows()

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Capture images using live camera')
    parser.add_argument('-c', '--camera_num', type=int, help='Specify the camera number of the camera that will be used in this program', default=0)
    parser.add_argument('-i', '--image_dir_path', help='Specify the absolute path to the directory where the images are to be stored', default='./Captured_images/')
    args = vars(parser.parse_args())
    # print(args)

    camera_cap = Camera_capture(camera_num=args['camera_num'], image_dir_path=args['image_dir_path'])
    camera_cap.start_cam()

    print("\nProgram execution ended!\n")
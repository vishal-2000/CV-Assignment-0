import argparse
from video_to_image import Video
from images_to_video import Images
import cv2
import numpy as np

class Chroma_key:
    def __init__(self, f_path: str, b_path: str, c_path: str, fps: int) -> None:
        '''
        Parameters:
        1. f_path: foreground video file path
        2. b_path: background video file path
        3. c_path: composite video file path
        4. fps: frames per second of final composte video
        '''
        self.f_path = f_path
        self.b_path = b_path
        self.c_path = c_path
        self.fps = fps

    def create_naive_composite(self, matte_color_range: list):
        '''
        This method simply turns the matte that falls in the given color range transparent so that the 
        opaque background video will take its position

        Parameters:
        1. matte_color_range: Color range of the holdout matte in foreground video

        Returns:
        None (Creates and stores the video in the specified c_path)
        '''
        # Load foreground and background as images and set matte color limits
        fg_video = Video(video_file_path=self.f_path)
        fg_img_array = fg_video.convert_to_images_and_return()
        bg_video = Video(video_file_path = self.b_path)
        bg_img_array = bg_video.convert_to_images_and_return()
        bg_img_array = bg_img_array[:1238]
        print(len(bg_img_array))
        print(len(fg_img_array))
        color_limits = matte_color_range

        # Start compositing the videos
        print("Compositing started!")
        img_res_array = []
        n_images = min(len(fg_img_array), len(bg_img_array))
        height, width, layers = fg_img_array[0].shape
        size = (width,height)
        print("Video file creation in process")
        if self.c_path == None:
            vid_writer = cv2.VideoWriter('./Joker_with_peter_result_fps={}.mp4'.format(self.fps), cv2.VideoWriter_fourcc(*'mp4v'), fps=int(self.fps), frameSize=size)
        else:
            vid_writer = cv2.VideoWriter(self.c_path, cv2.VideoWriter_fourcc(*'mp4v'), fps=int(self.fps), frameSize=size)

        for i in range(n_images):
            f_img = fg_img_array[i]
            b_img = bg_img_array[i]
            # Initialize the alpha channel and resize the images from the background video file
            alpha_channel = np.ones(shape=(f_img.shape[0], f_img.shape[1], 3))
            b_img = cv2.resize(b_img, ( f_img.shape[1], f_img.shape[0]))
            # Create masks based on holdout matte color (Vectorized and therefore very fast)
            red_ch_mask = np.logical_and(f_img[:, :, 0] >= matte_color_range[0][0], f_img[:, :, 0] <= matte_color_range[0][1])
            green_ch_mask = np.logical_and(f_img[:, :, 1] >= matte_color_range[1][0], f_img[:, :, 1] <= matte_color_range[1][1])
            blue_ch_mask = np.logical_and(f_img[:, :, 2] >= matte_color_range[2][0], f_img[:, :, 2] <= matte_color_range[2][1])
            # Update the alpha channel based on the masks created
            for i in range(3):
                alpha_channel[:, :, i] = np.logical_not(np.logical_and(np.logical_and(red_ch_mask, green_ch_mask), blue_ch_mask))
            # Add background image to the alpha multiplied foreground
            img_res = np.multiply(f_img, alpha_channel) + np.multiply(b_img, (1 - alpha_channel))
            img_res = img_res.astype(np.uint8)
            # cv2.imshow("image", img_res)
            # cv2.waitKey(0)
            # img_res_array.append(img_res)

            vid_writer.write(img_res)
        vid_writer.release()

        print("Saved!")

if __name__=='__main__':
    parser = argparse.ArgumentParser(description='Chroma keying (Compositing one video over another)')
    parser.add_argument('-f', '--foreground_video_path', help='Specify the absolute path to the foreground video file that is to be used', required=True)
    parser.add_argument('-b', '--background_video_path', help='Specify the absolute path to the background video file that is to be used', required=True)
    parser.add_argument('-v', '--composite_video_path', help='Specify the absolute path (with filename included) where the composite video is to be stored', required=True)
    parser.add_argument('-fps', '--frames_per_second', help='Specify the frames per second (integer > 0) of the composite video (by default, it uses 24)', default=24)
    parser.add_argument('-m', '--method', help='This variable sets what method to use to composite the two videos. Valid options include: \'naive\', \'vlahos\'. By default, \'naive\' method is used.', default='naive')
    parser.add_argument('-c', '--naive_method_matte_color_limits', help='If naive method is chosen, please input the color limits of the background matte used in the foreground image. By default, this is parrot green ([[0, 1], [204, 208], [0, 2]]) (Integers only)', type=int, default=[[0, 41],[230, 255],[0, 41]])# use this for the dinosaur video default=[[0, 1], [204, 208], [0, 2]])
    parser.add_argument('-k1', '--vlahos_method_k1', help='If vlahos method is chosen, please input the value of k1', default=0)
    parser.add_argument('-k2', '--vlahos_method_k2', help='If vlahos method is chosen, please input the value of k2', default=1)
    args = vars(parser.parse_args())
    print(args)

    # Create an instance of the chroma key class
    chroma_key = Chroma_key(f_path=args['foreground_video_path'], b_path=args['background_video_path'], c_path=args['composite_video_path'], 
                                fps=args['frames_per_second'])

    # check for the method and apply
    if args['method']=='naive':
        chroma_key.create_naive_composite(matte_color_range=args['naive_method_matte_color_limits'])
    elif args['method']=='vlahos':
        pass
    else:
        print("Invalid method name. Please use a valid method name. For more information, run 'python chroma_keying.py -h'")

    exit(0)
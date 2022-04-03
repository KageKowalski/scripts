# Converts a normal mp4 such that every frame becomes ascii art


# Imports
import cv2


def convert_mp4_to_ascii(mp4_path):
    pass


# Converts the frames of the mp4 with path mp4_file_in (String) to jpg images
# The jpg images are saved to the directory image_dir_out (String)
def convert_mp4_to_frames(mp4_file_in, image_dir_out):
    video_capture = cv2.VideoCapture(mp4_file_in)
    success, image = video_capture.read()
    count = 0
    while success:
        cv2.imwrite("{}frame{}.jpg".format(image_dir_out, count), image)
        success, image = video_capture.read()
        count = count + 1


def convert_frame_to_ascii(image_file):
    pass


def convert_ascii_to_mp4(image_files):
    pass

# Converts a normal mp4 such that every frame becomes ascii art


# Imports
import cv2
from pywhatkit import image_to_ascii_art


# Generates a new mp4 from mp4_file_in (String path to input mp4 file) where every frame is replaced with ascii art
# image_dir (String) is directory where temporary images should be stored
# mp4_file_out (String) is path + name of oupput mp4 file
def convert_mp4_to_ascii(mp4_file_in, image_dir, mp4_file_out):
    image_count = convert_mp4_to_frames(mp4_file_in, image_dir)

    for i in range(image_count):
        image_to_ascii_art("{}frame{}.jpg".format(image_dir, i), "{}ascii_frame{}.txt".format(image_dir, i))


# Converts the frames of the mp4 with path mp4_file_in (String) to jpg images
# The jpg images are saved to the directory image_dir_out (String)
# Returns number of images created (Int)
def convert_mp4_to_frames(mp4_file_in, image_dir_out):
    video_capture = cv2.VideoCapture(mp4_file_in)
    success, image = video_capture.read()
    count = 0
    while success:
        cv2.imwrite("{}frame{}.jpg".format(image_dir_out, count), image)
        success, image = video_capture.read()
        count = count + 1
    return count


def convert_ascii_to_mp4(image_files):
    pass

# Converts all frames of an mp4 to ascii art and prints the frames in the original video's framerate to cml


# Imports
import cv2
from PIL import Image
import time
from typing import Optional


# Generates a new mp4 from mp4_file_in (String path to input mp4 file) where every frame is replaced with ascii art
# image_dir (String) is directory where temporary images should be stored
# mp4_file_out (String) is path + name of output mp4 file
def build_dice_mp4(mp4_file_in, out_dir):
    image_count = convert_mp4_to_frames(mp4_file_in, image_dir)

    for i in range(image_count):
        image_to_ascii_art(f"{image_dir}frame{i}.jpg", f"{image_dir}ascii_frame{i}")

    fps = cv2.VideoCapture(mp4_file_in).get(cv2.CAP_PROP_FPS)
    for i in range(image_count):
        


# Converts the frames of the mp4 with path mp4_file_in (String) to jpg images
# The jpg images are saved to the directory image_dir_out (String)
# Returns number of images created (Int)
def convert_mp4_to_frames(mp4_file_in, image_dir_out):
    video_capture = cv2.VideoCapture(mp4_file_in)
    success, image = video_capture.read()
    count = 0
    while success:
        cv2.imwrite(f"{image_dir_out}frame{count}.jpg", image)
        success, image = video_capture.read()
        count = count + 1
    return count


# Ripped straight from pywhatkit; copying instead of importing avoids overhead
# First param is input file, second param is output file
def image_to_ascii_art():
    pass

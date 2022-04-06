# Contains scripts that are created with the intention of being fun rather than useful


# Imports
import os
from PIL import Image


# Converts image to ascii art
def image_to_ascii_art(image_name, image_path='.'):
    image_file = os.path.join(image_path, image_name)
    # Taken from mewbies.com
    chars = ['$', '@', 'B', '%', '8', '&', 'W', 'M', '#', '*', 'o', 'a', 'h', 'k', 'b', 'd', 'p', 'q', 'w', 'm', 'Z',
             'O', '0', 'Q', 'L', 'C', 'J', 'U', 'Y', 'X', 'z', 'c', 'v', 'u', 'n', 'x', 'r', 'j', 'f', 't', '/', '\\',
             '|', '(', ')', '1', '{', '}', '[', ']', '?', '-', '_', '+', '~', '<', '>', 'i', '!', 'l', 'I', ';', ':',
             ',', '\"', '^', '`', '\'', '.']

    # Load image, resize, and convert to greyscale
    image = Image.open(image_file)
    width, height = image.size
    aspect_ratio = height / width
    new_width = 120
    new_height = aspect_ratio * new_width * 0.55
    image = image.resize((new_width, int(new_height)))
    image = image.convert('L')

    # Get image pixels, convert to a string of characters, and split character string up into multiple strings
    pixels = image.getdata()
    new_pixels = [chars[pixel//25] for pixel in pixels]
    new_pixels = ''.join(new_pixels)
    new_pixels_count = len(new_pixels)
    ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
    ascii_image = '\n'.join(ascii_image)

    print(ascii_image)

    with open(os.path.join(image_path, f"{image_name}.txt"), 'w') as f:
        f.write(ascii_image)

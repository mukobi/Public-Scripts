"""Extends images to a square and fills the background with a blurred and darkened copy of the original image."""

import os
import argparse
from PIL import Image, ImageFilter, ImageEnhance

OUTPUT_DIMENSION = 3000
BLUR_SIZE = 42
DARKEN_FACTOR = 0.5
INCLUDED_FILE_EXTENSIONS = ['.jpg', '.jpeg', '.png']


def crop_to_square(img):
    """Minimally crop image to a centered square"""
    width, height = img.size
    if width == height:
        return img
    elif width > height:
        return img.crop(((width - height) / 2, 0, (width + height) / 2, height))
    else:
        return img.crop((0, (height - width) / 2, width, (height + width) / 2))


def extend(image):
    """Extend an image to a square with a transparent background"""
    width, height = image.size
    if width == height:
        return image
    elif width > height:
        result = Image.new('RGBA', (width, width), (0, 0, 0, 0))
        result.paste(image, (0, int((width - height) / 2)))
        return result
    else:
        result = Image.new('RGBA', (height, height), (0, 0, 0, 0))
        result.paste(image, (int((height - width) / 2), 0))
        return result


def main():
    '''Main execution function.'''

    # Get the input dir from user input
    input_dir = input(
        'Enter the folder path of the images you want to convert:\n')

    # Error checking
    if not os.path.exists(input_dir):
        print('Input path doesn\'t exist!')
        return

    output_dir = os.path.join(input_dir, 'square')
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Make filters
    blur_filter = ImageFilter.GaussianBlur(radius=BLUR_SIZE)

    # Get input images
    input_files = os.listdir(input_dir)

    # For each image in the input dir
    for image_filename in input_files:
        # Check that it's an image
        is_image = False
        for extension in INCLUDED_FILE_EXTENSIONS:
            if image_filename.lower().endswith(extension):
                is_image = True
        if not is_image:
            continue

        # Get the path of the image
        input_path = os.path.join(input_dir, image_filename)

        # Load the image
        background = Image.open(input_path)
        foreground = background.copy()

        # Crop the background to a square
        background = crop_to_square(background)

        # Resize it to the target size
        background = background.resize((OUTPUT_DIMENSION, OUTPUT_DIMENSION))

        # Blur it
        background = background.filter(blur_filter)

        # Darken it
        darken_enhancer = ImageEnhance.Brightness(background)
        background = darken_enhancer.enhance(DARKEN_FACTOR)

        # Composite the original image on top of it
        foreground = extend(foreground)
        foreground = foreground.resize((OUTPUT_DIMENSION, OUTPUT_DIMENSION))

        # background.paste(foreground, (background.size[0]/2 - foreground.size[0]/2, background.size[1]/2 - foreground.size[1]/2), foreground)
        background.paste(foreground, (0, 0), foreground)

        # Save the output
        image_name_no_ext = os.path.splitext(image_filename)[0]
        output_path = os.path.join(output_dir, f'{image_name_no_ext}.png')
        background.save(output_path)

        print(f'Processed {image_filename}')


if __name__ == '__main__':
    main()
    # input('Press enter to quit...')

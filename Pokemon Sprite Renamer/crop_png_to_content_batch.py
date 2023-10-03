"""
Crops images in a folder to the smallest square bounding box around the non-transparent content
and copies the cropped images to a new subfolder.
"""

import os
import shutil
from PIL import Image
from tqdm import tqdm


def main():
    """
    Main function to handle user input and image cropping.
    """
    # Ask user for folder path
    folder_path = input("Enter the folder path: ")

    # Create a subfolder in the input folder
    subfolder_path = os.path.join(folder_path, "cropped")

    # Clear the output folder if it exists
    if os.path.exists(subfolder_path):
        print(f"Clearing output folder {subfolder_path}")
        shutil.rmtree(subfolder_path)

    os.makedirs(subfolder_path, exist_ok=True)

    # Get list of files in the folder
    files = [
        f
        for f in os.listdir(folder_path)
        if f != "cropped"
        and (f.endswith(".png") or f.endswith(".jpg") or f.endswith(".jpeg"))
    ]

    # Iterate over files in the folder with a progress bar
    for filename in tqdm(files, desc="Cropping images"):
        try:
            # Open the image file
            img = Image.open(os.path.join(folder_path, filename))

            # Find the bounding box
            bbox = list(img.getbbox())

            # Expand the bbox until it's square in aspect ratio
            bbox_width = bbox[2] - bbox[0]
            bbox_height = bbox[3] - bbox[1]
            if bbox_width > bbox_height:
                # Expand the bbox vertically
                bbox[1] -= (bbox_width - bbox_height) / 2
                bbox[3] += (bbox_width - bbox_height) / 2
            elif bbox_height > bbox_width:
                # Expand the bbox horizontally
                bbox[0] -= (bbox_height - bbox_width) / 2
                bbox[2] += (bbox_height - bbox_width) / 2
            # Round the bbox to integers
            bbox = [int(coord) for coord in bbox]

            # Handle off-by-1 from rounding
            bbox_width = bbox[2] - bbox[0]
            bbox_height = bbox[3] - bbox[1]
            if bbox_width > bbox_height:
                bbox[3] = bbox[1] + bbox_width
            elif bbox_height > bbox_width:
                bbox[2] = bbox[0] + bbox_height

            # Crop the image to the bounding box
            cropped_img = img.crop(bbox)

            # Save the cropped image to the subfolder
            cropped_img.save(os.path.join(subfolder_path, filename))
        except Exception as exc:  # pylint: disable=broad-except
            tqdm.write(f"Error processing file {filename}: {exc}")

    print("Done cropping images.")


if __name__ == "__main__":
    main()

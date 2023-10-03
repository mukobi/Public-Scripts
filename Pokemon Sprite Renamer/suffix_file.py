"""
Appends a user-specified suffix to files in a folder, copies the renamed files to a new subfolder.
Useful for making Slack emojis.
"""

import os
import shutil
from tqdm import tqdm


def main():
    """
    Main function to handle user input and file renaming.
    """
    # Ask user for folder path and suffix
    folder_path = input("Enter the folder path: ")
    suffix = input("Enter the suffix: ")

    # Create a subfolder in the input folder
    subfolder_path = os.path.join(folder_path, "suffixed")

    # Clear the output folder if it exists
    if os.path.exists(subfolder_path):
        print(f"Clearing output folder {subfolder_path}")
        shutil.rmtree(subfolder_path)

    os.makedirs(subfolder_path, exist_ok=True)

    # Get list of files in the folder
    files = [f for f in os.listdir(folder_path) if f != "suffixed"]

    # Iterate over files in the folder with a progress bar
    for filename in tqdm(files, desc="Suffixing files"):
        try:
            # Extract the number and extra data from the filename
            name, extension = os.path.splitext(filename)
            new_filename = f"{name}{suffix}{extension}"

            # Copy the file to the subfolder with the new name
            shutil.copy(
                os.path.join(folder_path, filename),
                os.path.join(subfolder_path, new_filename),
            )
        except Exception as exc:  # pylint: disable=broad-except
            tqdm.write(f"Error processing file {filename}: {exc}")

    print("Done suffixing files.")


if __name__ == "__main__":
    main()

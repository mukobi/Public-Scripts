"""
This script renames Pokemon sprite images based on their Pokedex index,
appends a user-specified suffix, and copies the renamed files to a new subfolder.
Useful for making Slack emojis.
Download sprite packs from https://veekun.com/dex/downloads
"""

import os
import shutil
import requests
from tqdm import tqdm


def get_pokemon_name(index):
    """
    Fetches the Pokemon name corresponding to a given Pokedex index from the PokeAPI.

    Args:
        index (int): The Pokedex index of the Pokemon.

    Returns:
        str: The name of the Pokemon.
    """
    response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{index}")
    return response.json()["name"]


def main():
    """
    Main function to handle user input and file renaming.
    """
    # Ask user for folder path and suffix
    folder_path = input("Enter the folder path: ")
    suffix = input("Enter the suffix: ")

    # Create a subfolder in the input folder
    subfolder_path = os.path.join(folder_path, "renamed_pokemon")

    # Clear the output folder if it exists
    if os.path.exists(subfolder_path):
        print(f"Clearing output folder {subfolder_path}")
        shutil.rmtree(subfolder_path)

    os.makedirs(subfolder_path, exist_ok=True)


    # Get list of files in the folder
    files = [f for f in os.listdir(folder_path) if f != "renamed_pokemon"]

    # Iterate over files in the folder with a progress bar
    for filename in tqdm(files, desc="Renaming files"):
        try:
            # Extract the number and extra data from the filename
            name, extension = os.path.splitext(filename)
            number, *extra_data = name.split("-")

            # Get the Pokemon name
            pokemon_name = get_pokemon_name(int(number))

            # Create the new filename
            new_filename = f"{int(number):03d}-{pokemon_name}"
            if extra_data:
                new_filename += f"-{'-'.join(extra_data)}"
            new_filename += f"-{suffix}{extension}"

            # Copy the file to the subfolder with the new name
            shutil.copy(os.path.join(folder_path, filename), os.path.join(subfolder_path, new_filename))
        except Exception as exc:
            tqdm.write(f"Error processing file {filename}: {exc}")

    print("Done renaming files.")


if __name__ == "__main__":
    main()

import requests
import tempfile
import shutil
import zipfile
import os


def download_and_extract_zip(url, new_location):
    # Create a temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        zip_path = os.path.join(temp_dir, "downloaded.zip")

        # Download the zip file
        response = requests.get(url)
        with open(zip_path, 'wb') as f:
            f.write(response.content)

        # Extract the zip file
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(temp_dir)

        # The first directory inside the zip file (assuming there's only one top-level directory)
        extracted_dir = next(
            os.path.join(temp_dir, d) for d in os.listdir(temp_dir) if os.path.isdir(os.path.join(temp_dir, d)))

        # New path for the top-level directory

        # Copy the contents to the new location with a new top-level directory name
        shutil.copytree(extracted_dir, new_location, dirs_exist_ok=True)

        # Remove the temporary directory
        shutil.rmtree(temp_dir)


from pathlib import Path

def find_file_path(directory, filename):
    """
    Search for all instances of the specified directory in the given directory and its subdirectories,
    and return the one with the shortest path (least depth).

    Parameters:
    - directory: The root directory to start the search from, as a string or a Path object.
    - dir_name: The name of the directory to search for.

    Returns:
    - The full path to the shallowest instance of the specified directory if found, otherwise None.
    """
    directory_path = Path(directory)
    matching_dirs = [path for path in directory_path.rglob(filename) ]

    if not matching_dirs:
        return None

    # Select the directory with the shortest path
    shallowest_dir = min(matching_dirs, key=lambda path: len(path.parts))
    return shallowest_dir

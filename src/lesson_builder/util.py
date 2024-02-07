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
        shutil.copytree(extracted_dir, new_location)

        # Remove the temporary directory
        shutil.rmtree(temp_dir)



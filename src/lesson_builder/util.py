from dataclasses import dataclass

import requests
import tempfile
import shutil
import zipfile
import os
import inspect

import yaml

import logging
logger = logging.getLogger('lesson-builder')

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


@dataclass
class ResourceWrite:
    source: Path | str | bytes
    dest: Path
    file: str = None
    line: int = None


    def __post_init__(self):
        if isinstance(self.source, Path):
            assert self.source.exists(), f"Source file {self.source} does not exist"

    @property
    def is_render(self):
        return isinstance(self.source, dict)

    def render(self):
        from .render import render
        rw = ResourceWrite(render(**self.source), self.dest)
        rw.write()

    def write(self):

        if isinstance(self.source, Path):

            if self.source.is_file():
                self.dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy(self.source, self.dest)
            else:
                shutil.copytree(self.source, self.dest, dirs_exist_ok=True)

        elif isinstance(self.source, str):
            self.dest.parent.mkdir(parents=True, exist_ok=True)
            self.dest.write_text(self.source)
        elif isinstance(self.source, bytes):
            self.dest.parent.mkdir(parents=True, exist_ok=True)
            self.dest.write_bytes(self.source)
        else:
            pass  # it is a render, save it for later.

    def as_str(self, root: Path):
        if isinstance(self.source, Path):
            src = self.source.relative_to(root)

        elif isinstance(self.source, str):
            src = f"<{len(self.source)} bytes>"
        elif isinstance(self.source, dict):
            src = f"<Render {self.source['working_directory'].name}>"

        dst = self.dest.relative_to(root)

        return f"{src} -> {dst}"

    def __str__(self):
        if isinstance(self.source, Path):
            src = self.source # str(self.source)

        elif isinstance(self.source, str):
            src = f"<{len(self.source)} bytes>"
        elif isinstance(self.source, dict):
            src = f"<Render {self.source['working_directory'].name}>"

        dst = str(self.dest)

        return f"{src} -> {dst}"


def get_first_h1_heading(markdown_file_path):
    """
    Extracts the text of the first h1 heading from a markdown file.

    Parameters:
    markdown_file_path (str): The path to the markdown file.

    Returns:
    str: The text of the first h1 heading, or None if no h1 heading is found.
    """
    try:
        with open(markdown_file_path, 'r', encoding='utf-8') as file:
            for line in file:
                # Check if the line starts with '# ' indicating an h1 heading
                if line.startswith('# '):
                    # Return the text following '# ' (strip removes leading and trailing whitespace)

                    return line.strip()[2:]
    except FileNotFoundError:
        print(f"File not found: {markdown_file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")

    # Return None if no h1 heading is found
    return None


def get_repo_root():
    from plumbum.cmd import git

    repo_name = git("rev-parse", "--show-toplevel").split('/')[-1].strip()

    rr = Path.cwd()

    assert repo_name == 'java-modules' and (rr / 'levels').exists(), "Not in the java-modules repo"

    return rr


def build_dir(level, module=None):
    rr = get_repo_root()

    level = level.title()

    if module is None:
        return rr / '_build' / 'levels' / level
    else:
        module = module.title()
        return rr / '_build' / 'modules' / level / module

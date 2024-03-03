import json
import re
import shutil
from pathlib import Path
from textwrap import dedent

from .walk import get_lm

def copy_dir(from_, base):
    parts = from_.name.split('-')
    level = parts[0]
    module = parts[1]
    to = base / level / module

    shutil.copytree(from_, to )


def find_java_main_files(start_path):
    """
    Walks through the directory tree starting from start_path and yields the Path
    of each Java source file (.java) that contains a main() method.

    Args:
    - start_path (str or Path): The root directory from which to start searching.

    Yields:
    - Path objects pointing to Java files with a main() method.
    """
    start_path = Path(start_path)  # Ensure start_path is a Path object
    pattern = re.compile(r'public\s+static\s+void\s+main\s*\(\s*String\s*\[\s*\]\s+\w+\s*\)')  # Regex to match the main method

    for path in start_path.rglob('*.java'):  # rglob method for recursive globbing
        with open(path, 'r', encoding='utf-8') as file:
            if pattern.search(file.read()):  # Check if the file contains a main() method
                rp = str(path).split('/src/', 1)[-1]
                try:
                    package, clazz = rp.rsplit('/', 1)
                    clazz = clazz.replace('.java','')
                    package = package.replace('/','.')
                    fqn = '.'.join(package.split('.')+[clazz])
                    yield path, package, clazz, fqn
                except ValueError:
                    print("ERROR: Can't process class package", path)


def _move_jars_to_root(root):
    """Actually move the jar files into the lib dir"""
    root = Path(root)

    jars = list(Path(root).glob("**/*.jar"))

    if jars:

        (Path(root) / 'lib').mkdir(exist_ok=True)

        for jar in jars:
            jar.rename(root/"lib"/jar.name)

        (Path(root) / 'lib' / 'jars.txt').write_text('\n'.join([e.name for e in jars])+'\n')


def write_classpath(dir_):
    """Write the eclipse classpath file"""

    dir_ = Path(dir_)

    jf = (dir_/"lib"/"jars.txt")

    if not jf.exists():
        return

    # Do we need this?
    container = dedent(f"""
    <classpathentry kind="con" path="org.eclipse.jdt.launching.JRE_CONTAINER/org.eclipse.jdt.internal.debug.ui.launcher.StandardVMType/JavaSE-1.8">
        <attributes>
            <attribute name="module" value="true"/>
        </attributes>
    </classpathentry>
    """).strip()

    jars_s = ''

    for jar in jf.read_text().splitlines():
        jars_s += f'    <classpathentry kind="lib" path="lib/{jar}"/>\n    '

    cp = dedent(f"""
    <?xml version="1.0" encoding="UTF-8"?>
    <classpath>
        <classpathentry kind="src" path="src"/>
        <classpathentry kind="src" path="images"/>
        <classpathentry kind="output" path="bin"/>
    {jars_s}
    </classpath>
    """).strip()

    (dir_/'.classpath').write_text(cp)


def write_settings(dir_):
    """Write the VSCode settings file"""

    sf = (dir_/".vscode"/"settings.json")

    sf.parent.mkdir(exist_ok=True)

    sf_s = dedent(f"""
    {{
        "java.project.sourcePaths": [
            "images",
            "src"
        ],
        "java.project.outputPath": "bin",
        "java.project.referencedLibraries": [
            "lib/**/*.jar"
        ]
    }}
    """).strip()

    sf.write_text(sf_s+'\n')


def write_gitignore(dir_):
    gi_s = dedent(f"""
    *.class
    bin/*
    !bin/.keep
    .DS_Store
                  
    """).strip()

    (dir_/'.gitignore').write_text(gi_s+'\n')

def write_launch(dir_):
    """Write the VSCode launch.json file"""
    configs = []

    for path, package, clazz, fqn  in find_java_main_files(dir_):
            if clazz not in ('LeagueToken',):
                configs.append(
                    {
                        "type": "java",
                        "name": clazz,
                        "request": "launch",
                        "mainClass": fqn
                    }
                )

    configs = list(sorted(configs, key=lambda e: e['name']))

    lc = {
        "version": "0.2.0",
        "configurations": configs
    }

    (dir_/".vscode"/"launch.json").write_text(json.dumps(lc, indent=4))


def make_dirs(dir_):
    dirs = ['lib','src','images', 'bin']
    for d in dirs:
        p  = dir_/d
        if not p.exists():
            p.mkdir()
            (p/".keep").touch()


def copy_devcontainer(repo_root, dir_):
    """Copy the devcontainer file from the root into the module"""
    source = repo_root/'.devcontainer'
    dest = dir_/".devcontainer"

    if not source.exists():
        raise FileNotFoundError(source)

    dest.mkdir(exist_ok=True)

    shutil.copy(source/'devcontainer-module.json', dest/'devcontainer.json')


def copy_scripts(dir_):

    source = Path('./scripts')
    dest = dir_/"scripts"

    if not source.exists():
        raise FileNotFoundError(source)

    dest.mkdir(exist_ok=True)

    shutil.copytree(source, dest, dirs_exist_ok=True)


def disable_eclipse(dir_):

    if not (p := Path(dir_)/'.eclipse').exists():
        p.mkdir(parents=True)

    for f in ('.settings', '.classpath', '.project'):
        if ( p:=Path(dir_)/f).exists():
            p.rename(Path(dir_)/'.eclipse'/f)


def make_repo_template(dir_=None, owner="League-Java"):
    """
;/"{{""}}"
    Parameters:
    - owner: str. The username of the repository owner.
    - repo: str. The name of the repository.

    """

    l, m = get_lm(dir_)

    repo = f"{l}-{m}"

    github_token = os.environ['GITHUB_TOKEN']


    assert github_token is not None

    url = f"https://api.github.com/repos/{owner}/{repo}"
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    data = {"is_template": True}

    response = requests.patch(url, headers=headers, json=data)

    if response.status_code == 200:
        print(f"The repository '{repo}' has been successfully turned into a template.")
    else:
        print(f"Failed to turn the repository into a template. Status code: {response.status_code}, Response: {response.text}")


def extract_urls(script_text):
    # Regular expression to match document.location.href redirection URLs
    pattern = r'document\.location\.href\s*=\s*"([^"]+)"'

    # Find all non-overlapping matches in the script text
    urls = re.findall(pattern, script_text)

    return urls

import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin


def get_url(url):
    response = requests.get(url)
    return response.text

def download_webpage_assets(url_or_text, save_dir):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    if url_or_text.startswith("http"):
        url = url_or_text
        html_content = get_url(url_or_text)
    else:
        url = None
        html_content = url_or_text

    # Parse HTML using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Find and download all images
    for img in soup.find_all('img'):
        img_url = img.get('src')
        if img_url:
            # Convert relative URLs to absolute URLs
            if url and not img_url.startswith('http'):
                full_img_url = urljoin(url, img_url)
            else:
                full_img_url = img_url

            img_data = requests.get(full_img_url).content
            img_name = os.path.basename(img_url)
            img_save_path = os.path.join(save_dir, img_name)

            # Remove any query parameters from the image name
            img_save_path = img_save_path.split('?')[0]

            with open(img_save_path, 'wb') as img_file:
                img_file.write(img_data)
                print(f'Downloaded {img_name}')

    # Save the modified HTML file
    html_save_path = os.path.join(save_dir, 'index.html')
    with open(html_save_path, 'w', encoding='utf-8') as html_file:
        html_file.write(html_content)
        print(f'HTML saved to {html_save_path}')

def compile_meta(metas):
    """Reorganize metadata in a heirarchy"""
    levels = {}

    for meta in metas:

        l, m, ls, a = meta['level'], meta['module'], meta['lesson'], meta['assignment']

        if l not in levels:
            levels[l] = {}

        if m not in levels[l]:
            levels[l][m] = {}

        if ls not in levels[l][m]:
            levels[l][m][ls] = []

        levels[l][m][ls].append(meta)

    return levels
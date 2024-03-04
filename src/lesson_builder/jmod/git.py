import logging
import shutil
from pathlib import Path

from plumbum import local, FG
from plumbum.cmd import gh, git

from lesson_builder.config import site_template_url
from lesson_builder.jmod.walk import get_lm

logger = logging.getLogger(__name__)


def repo_exists(org, repo):
    url = f"{org}/{repo}"

    try:
        gh("repo", "view", url, "--json", "url")
    except Exception:  # If the command fails, the repo does not exist
        return False
    else:
        return True


def clone_or_pull_repo(org: str, repo: str, dest: str | Path):
    dest = Path(dest)

    if not dest.exists():
        dest.mkdir(parents=True)

    if not (dest / repo).exists():
        with local.cwd(dest):
            gh("repo", "clone", f"{org}/{repo}")
            logger.info(f"Cloned {org}/{repo} to {dest}")

    else:
        with local.cwd(dest / repo):
            git("pull")
            logger.info(f"Pulled {org}/{repo} to {dest}")


def new_vuepress(level, dest_org="League-Java"):
    from time import sleep

    if not repo_exists(dest_org, level):
        dest = f"{dest_org}/{level}"
        gh("repo", "create", dest, "--template", site_template_url,
           "--public")
        logger.info(f"Created vurepress site at repo {dest}")

        sleep(5)  # Wait for github.com to get the repo ready


def create_repo(dir_: str | Path, org: str, build_dir: str | Path):
    """
    Create a repository on GitHub and push the contents of dir_
    Args:
        dir_ ():
        org ():
        build_dir ():

    Returns:

    """
    from .util import build_dir

    l, m = get_lm(dir_)
    repo = f"{l}-{m}"
    url = f'https://github.com/{org}/{repo}.git'

    target_dir = build_dir(l, m)

    if target_dir.exists():
        shutil.rmtree(target_dir)

    shutil.copytree(dir_, target_dir)

    with local.cwd(target_dir):

        print("Pushing ", target_dir)

        if not (target_dir / Path('.git')).exists():
            logger.info(f"    Create local repo {repo}")
            git("init")
            git("add", "-A")
            git("commit", "-m", "Initial commit")
        else:
            logger.info(f"    Local repo {repo} exists, updating")
            git("add", "-A")
            git("commit", "-m", "Updating")

        if not repo_exists(org, repo):
            gh("repo", "create", f"{org}/{repo}", "--public", "-s", ".")
            logger.info(f"    Created remote repo {repo}")
        else:
            logger.info(f"    Remote repo {repo} already exists")

        # Check if the remote origin exists
        try:
            (git["remote", "-v"] | grep["origin"]) & FG
        except Exception:
            logger.info(f"    Add remote origin {url}")
            git("remote", "add", "origin", url)

        logger.info("    Push")
        git("push", "-f", "--set-upstream", "origin", "master")

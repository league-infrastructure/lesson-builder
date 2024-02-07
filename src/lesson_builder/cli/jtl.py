# Main entry point for building and reporting on the
# lesson website.

__author__ = "Eric Busboom"
__copyright__ = "Eric Busboom"
__license__ = "MIT"

import logging
import os
from pathlib import Path

import click
from plumbum import local, FG
from plumbum.cmd import yarn, git
from plumbum.commands.processes import ProcessExecutionError
from slugify import slugify

from lesson_builder.lesson import LessonPlan
from lesson_builder.lesson import logger as lesson_logger
from lesson_builder.util import download_and_extract_zip

logger = logging.getLogger(__name__)


assignment_template_url = 'https://github.com/league-python/PythonLessons/raw/master/templates/assignment_template.zip'
lesson_template_url = 'https://github.com/league-python/PythonLessons/raw/master/templates/lesson_template.zip'

@click.group()
@click.option('-v', '--verbose', is_flag=True, show_default=True, default=False, help="INFO logging")
@click.option('-vv', '--debug', is_flag=True, show_default=True, default=False, help="DEBUG logging")
def main(verbose: bool, debug: bool):
    if debug:
        logging.basicConfig()
        logger.setLevel(logging.DEBUG)
        lesson_logger.setLevel(logging.DEBUG)
    elif verbose:
        logging.basicConfig()
        logger.setLevel(logging.INFO)
        lesson_logger.setLevel(logging.INFo)


def check_dirs(lesson_path: str = None, docs_path=None, assignments_path=None):
    if lesson_path is None:
        lesson_path = Path.cwd() / 'lessons'

    lesson_path = Path(lesson_path)

    if docs_path is None:
        docs_path = Path.cwd() / 'docs/src'

    docs_path = Path(docs_path)

    if assignments_path is None:
        assignments_path = Path.cwd()

    assignments_path = Path(assignments_path)

    if not lesson_path.exists():
        raise FileNotFoundError(f"Lesson path {lesson_path} does not exist")

    if not docs_path.exists():
        raise FileNotFoundError(f"Docs path {docs_path} does not exist")

    if not docs_path / 'src/.vuepress':
        raise FileNotFoundError(f"Vuepress dir '.vuepress' not found in {docs_path}")

    if not assignments_path.exists():
        raise FileNotFoundError(f"Assignments path {assignments_path} does not exist")

    if not assignments_path / 'lesson-plan.yaml':
        raise FileNotFoundError(f"Lesson plan 'lesson-plan.yaml' not found in {lesson_path}")

    return lesson_path, docs_path, assignments_path


@main.command(help="Build the website from the lesson plan")
@click.option('-l', '--lesson', 'lesson_path', help='Path to the lesson plan directory')
@click.option('-d', '--docs', 'docs_path', help='Path to the root of the vuepress docs directory ( one above src )')
@click.option('-a', '--assignments', 'assignments_path', help='Path to the assignments directory')
@click.option('-b', '--url_base', 'url_base', default=None,
              help='Set the basedir for the url, often needed '
                   'for Github pages. Defaults to name of repository. Use "/" for root.')
def build(lesson_path: str = None, docs_path=None, assignments_path=None, url_base=None):
    """Build the website from the lesson plan

    Args:
        lesson_path (str): The path to the lesson plan. If not specified, the default is 'lessons'
        docs_path (str): The path to the docs directory. If not specified, the default is 'docs/src'
        assignments_path (str): The path to the assignments directory. If not specified, the default is 'assignments'
    """

    lesson_path, docs_path, assignments_path = check_dirs(lesson_path, docs_path, assignments_path)

    lp = LessonPlan(lesson_path, docs_path, assignments_path, less_subdir='lessons')

    if url_base is None or url_base is False:
        origin_url = git('remote', 'get-url', 'origin').strip()
        url_base = Path(origin_url).stem
        logger.info(f"Using url base '{url_base}'")
    elif url_base == '/':
        url_base = None

    lp.build(url_base_dir=url_base)


@main.command(help="Print configuration (tbd)")
def config():
    print("reporting!")


@main.command(help="Deploy the website to Github Pages")
@click.option('-d', '--docs', 'docs_path', help='Path to the root of the vuepress docs directory ( one above src )')
def deploy(docs_path=None):
    # Workaround errors on build due to openssl issues in Node 17
    # Maybe need to set this extern to the call:
    # NODE_OPTIONS=--openssl-legacy-provider ./jtl deploy

    os.environ['NODE_OPTIONS'] = '--openssl-legacy-provider'

    origin_url = git('remote', 'get-url', 'origin').strip()

    if docs_path is None:
        docs_path = Path.cwd() / 'docs'
    else:
        docs_path = Path(docs_path)

    try:
        with local.cwd(docs_path):
            yarn['build'] & FG

        with local.cwd(docs_path / 'src/.vuepress/dist'):
            git['init'] & FG
            git['add', '-A'] & FG
            git['commit', '-m', 'deploy'] & FG
            git['push', '-f', origin_url, 'master:gh-pages'] & FG

    except ProcessExecutionError as e:

        print(f"Command failed with exit code {e.retcode}: {e}")

        exit(e.retcode)


@click.option('-d', '--docs', 'docs_path', help='Path to the root of the vuepress docs directory ( one above src )')
@main.command(help="Run the development server")
def serve(docs_path=None):
    from plumbum import local, FG
    from plumbum.cmd import yarn

    if docs_path is None:
        docs_path = Path.cwd() / 'docs'
    else:
        docs_path = Path(docs_path)

    with local.cwd(docs_path):
        yarn['dev'] & FG


@main.group(help='create new lesson plans and assignments')
def new():
    pass


@new.command(name='plan', help="Create a new lesson plan")
@click.option('--count', default=1, help='number of greetings')
@click.argument('name')
def new_lessonplan(name: str):

    title = slugify(name, separator='_')

    print("New Lesson Plan", title)

    if Path(title).exists():
        raise FileExistsError(f"Lesson {title} already exists")

    download_and_extract_zip(lesson_template_url, title)

@new.command(name='assignment', help="Create a new assignment")
@click.argument('name')
def new_assignment(name: str):

    title = slugify(name, separator='_')

    print("New Assignment",title)

    if Path(title).exists():
        raise FileExistsError(f"Assignment {title} already exists")

    download_and_extract_zip(assignment_template_url, title)



if __name__ == '__main__':
    main()

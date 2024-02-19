# Main entry point for building and reporting on the
# lesson website.

__author__ = "Eric Busboom"
__copyright__ = "Eric Busboom"
__license__ = "MIT"

import logging
import os
import shutil
from pathlib import Path
from lesson_builder.util import find_file_path
import yaml

import click
from plumbum import local, FG
from plumbum.cmd import yarn, git
from plumbum.commands.processes import ProcessExecutionError
from slugify import slugify
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

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
        lesson_logger.setLevel(logging.INFO)

def check_dirs(lesson_path: str = None, docs_path=None, assignments_path=None):
    if lesson_path is None:
        lesson_path = Path.cwd() / 'lessons'

    lesson_path = Path(lesson_path)

    if docs_path is None:
        vp = find_file_path(Path.cwd(), '.vuepress')
        if not vp:
            raise FileNotFoundError(f"Vuepress dir '.vuepress' not found in {Path.cwd()}")

        docs_path = vp.parent.parent

    docs_path = Path(docs_path)

    if assignments_path is None:
        assignments_path = lesson_path

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
@click.option('-w','--watch', is_flag=True, default=False, help='Rebuild when source files change')
def build(lesson_path: str = None, docs_path=None, assignments_path=None,
          url_base=None, watch=False):
    """Build the website from the lesson plan

    Args:
        lesson_path (str): The path to the lesson plan. If not specified, the default is 'lessons'
        docs_path (str): The path to the docs directory. If not specified, the default is 'docs/src'
        assignments_path (str): The path to the assignments directory. If not specified, the default is 'assignments'
    """

    lesson_path, docs_path, assignments_path = check_dirs(lesson_path, docs_path, assignments_path)


    if url_base is None or url_base is False:
        origin_url = git('remote', 'get-url', 'origin').strip()
        url_base = Path(origin_url).stem
        logger.info(f"Using url base '{url_base}'")
    elif url_base == '/':
        url_base = None

    # Always build once first,
    lp = LessonPlan(lesson_path, docs_path, assignments_path, less_subdir='lessons')
    lp.build(url_base_dir=url_base)

    if  watch:

        class RebuildHandler(FileSystemEventHandler):
            def on_any_event(self, event):
                if not event.src_path.endswith('~') and Path(event.src_path).is_file():
                    lp = LessonPlan(lesson_path, docs_path, assignments_path, less_subdir='lessons')
                    lp.build(url_base_dir=url_base)

        event_handler = RebuildHandler()
        observer = Observer()
        observer.schedule(event_handler, assignments_path, recursive=True)
        observer.schedule(event_handler, lesson_path, recursive=True)
        observer.start()
        try:
            while observer.is_alive():
                observer.join(1)
        finally:
            observer.stop()
            observer.join()


@main.command(help="Print configuration (tbd)")
def config():
    from lesson_builder import __version__
    print(f"Lesson Builder version {__version__}")


@main.command(help="Creates and configures a new vewpress docs dir")
@click.option('-r', '--root', 'root_path',
              help='Path to the dir tht will hold docs, defaults to current dir')
def installvp(root_path=None):

    if root_path is None:
        root_path = Path.cwd()
    else:
        root_path = Path(root_path)

    # yarn create vuepress-site && (cd docs && yarn install)
    with local.cwd(root_path):
        yarn['create','vuepress-site'] & FG

    with local.cwd(root_path / 'docs'):
        yarn['install'] & FG





@main.command(help="Run the development server")
@click.option('-d', '--docs', 'docs_path', help='Path to the root of the vuepress docs directory ( one above src )')

def serve(docs_path=None):
    from plumbum import local, FG, BG
    from plumbum.cmd import yarn

    if docs_path is None:
        docs_path = Path.cwd() / 'docs'
    else:
        docs_path = Path(docs_path)

    with local.cwd(docs_path):
        yarn['dev'] & FG


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

        dist = docs_path / 'src/.vuepress/dist'

        with local.cwd(dist):
            open(dist / '.nojekyll', 'a').close()
            git['init'] & FG
            git['add', '-A'] & FG
            git['commit', '-m', 'deploy'] & FG
            git['push', '-f', origin_url, 'master:gh-pages'] & FG



    except ProcessExecutionError as e:

        print(f"Command failed with exit code {e.retcode}: {e}")
        print("⚠️  This is a known issue with Node 17 and openssl. Try setting NODE_OPTIONS=--openssl-legacy-provider")
        print("For instance: ")
        print("    NODE_OPTIONS=--openssl-legacy-provider jtl deploy")
        exit(e.retcode)

@main.group(help='create new lesson plans and assignments')
def new():
    pass


@new.command(name='plan', help="Create a new lesson plan")
@click.option('-F', '--force', is_flag=True, show_default=True, default=False,
              help="Overwrite existing lesson plan")
@click.argument('name')
def new_lessonplan(name: str, force: bool):

    title = slugify(name, separator='_')

    print("New Lesson Plan", title)

    if Path(title).exists() and not force:
        raise FileExistsError(f"Lesson {title} already exists")

    download_and_extract_zip(lesson_template_url, title)

@new.command(name='assignment', help="Create a new assignment")
@click.option('-F', '--force', is_flag=True, show_default=True, default=False,
              help="Overwrite existing assignment")
@click.argument('name')
def new_assignment(name: str, force: bool = False):

    title = slugify(name, separator='_')

    print("New Assignment",title)

    if Path(title).exists():
        if force:
            shutil.rmtree(title)
        else:
            raise FileExistsError(f"Assignment {title} already exists")

    download_and_extract_zip(assignment_template_url, title)

    asgn_file = Path(title) / "_assignment.yaml"

    d = yaml.safe_load(asgn_file.read_text())

    d['title'] = name
    d['description'] = name

    # These should be removed from the source file,
    # but well do it here for now.
    if 'level' in d:
        del d['level']

    if 'module' in d:
        del d['module']

    if 'lesson' in d:
        del d['lesson']

    asgn_file.write_text(yaml.safe_dump(d))

if __name__ == '__main__':
    main()

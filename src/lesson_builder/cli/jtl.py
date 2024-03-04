# Main entry point for building and reporting on the
# lesson website.

__author__ = "Eric Busboom"
__copyright__ = "The League of Amazing Programmers"
__license__ = "MIT"

import logging
import os
import shutil
from pathlib import Path
from textwrap import dedent

import click
import yaml
from plumbum import local, FG
from plumbum.cmd import yarn, git
from plumbum.commands.processes import ProcessExecutionError
from slugify import slugify
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from lesson_builder.buildlevels import make_lessons
from lesson_builder.config import assignment_template_url, lesson_template_url
from lesson_builder.jmod.git import clone_or_pull_repo, new_vuepress
from lesson_builder.jmod.git import logger as git_logger
from lesson_builder.jmod.tasks import update_meta
from lesson_builder.lesson import logger as lesson_logger
from lesson_builder.lesson_plan import LessonPlan
from lesson_builder.util import download_and_extract_zip, find_file_path, get_repo_root, build_dir
from lesson_builder.util import logger
from lesson_builder.jmod.git import create_repo

show_exceptions = False


@click.group()
@click.option('-v', '--verbose', is_flag=True, show_default=True, default=False, help="INFO logging")
@click.option('-vv', '--debug', is_flag=True, show_default=True, default=False, help="DEBUG logging")
@click.option('-E', '--exceptions', is_flag=True, show_default=True, default=False,
              help="Display exception stack traces")
def main(verbose: bool, debug: bool, exceptions: bool):
    if debug:
        logging.basicConfig()
        logger.setLevel(logging.DEBUG)
        lesson_logger.setLevel(logging.DEBUG)
        git_logger.setLevel(logging.DEBUG)
    elif verbose:
        logging.basicConfig()
        logger.setLevel(logging.INFO)
        lesson_logger.setLevel(logging.INFO)
        git_logger.setLevel(logging.INFO)

    global show_exceptions
    show_exceptions = exceptions


def main_entry():
    try:
        main()
    except Exception as e:
        if show_exceptions:
            raise
        else:
            click.echo(f"Error: {e}")


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
@click.option('-Y', '--yarn-build', is_flag=True, default=False, help='Also run Yarn Build')
@click.option('-w', '--watch', is_flag=True, default=False, help='Rebuild when source files change')
def build(lesson_path: str = None, docs_path=None, assignments_path=None,
          url_base=None, yarn_build=False, watch=False):
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
    lp.update_config(basedir=url_base)
    lp.build(url_base_dir=url_base)

    if yarn_build:
        with local.cwd(docs_path):
            yarn['build'] & FG

    dist = docs_path / 'src/.vuepress/dist'

    if watch:

        class RebuildHandler(FileSystemEventHandler):
            def on_any_event(self, event):
                if not event.src_path.endswith('~') and Path(event.src_path).is_file():
                    lp = LessonPlan(lesson_path, docs_path, assignments_path, less_subdir='lessons')

                    try:
                        lp.build(url_base_dir=url_base)

                        if yarn_build:
                            with local.cwd(docs_path):
                                yarn['build'] & FG

                    except Exception as e:
                        logger.error(f"Error building: {e}")

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

    elif yarn_build:
        print("Built to ", dist)


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
        yarn['create', 'vuepress-site'] & FG

    with local.cwd(root_path / 'docs'):
        yarn['install'] & FG


@main.command(help="Run the development server")
@click.option('-d', '--docs', 'docs_path', help='Path to the root of the vuepress docs directory ( one above src )')
def serve(docs_path=None):
    from plumbum import local, FG
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

    if docs_path is None:
        docs_path = Path.cwd() / 'docs'
    else:
        docs_path = Path(docs_path)

    config_path = docs_path / 'src/.vuepress/config.yml'
    config = yaml.safe_load(config_path.read_text())

    try:
        with local.cwd(docs_path):
            origin_url = git('remote', 'get-url', 'origin').strip()
            yarn['build'] & FG

        dist = docs_path / 'src/.vuepress/dist'

        with local.cwd(dist):
            if 'cname' in config:
                (dist / 'CNAME').write_text(config['cname'])

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
        print("    export NODE_OPTIONS=--openssl-legacy-provider")
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
@click.option('-d', '--dir', is_flag=True, show_default=True, default=False,
              help="Create a directory assignment. Otherwise, create a file assignment.")
@click.argument('name')
def new_assignment(name: str, dir: bool = False, force: bool = False):
    slug = slugify(name, separator='_')

    print("New Assignment", slug)

    if Path(slug).exists() or Path(slug).with_suffix('.md').exists():

        if force:
            if Path(slug).exists():
                shutil.rmtree(slug)
            else:
                (Path(slug).with_suffix('.md')).unlink()
        else:
            raise FileExistsError(f"Assignment {slug} already exists")

    if dir:
        download_and_extract_zip(assignment_template_url, slug)

        asgn_file = Path(slug) / "_assignment.yaml"

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

        if (Path(slug) / "goal.png").exists():
            (Path(slug) / "goal.png").unlink()

        tfile = Path(slug) / "trinket.md"

        tfile.write_text(dedent(f"""
        # {name}
        
        {{{{ trinket("python_program.py", width="100%", height="600", embed_type="python") | safe }}}}
        
        """).strip())

    else:

        t = dedent(f"""
        # {name}
        
        ```python.run
        print("Hello, World!")
        ```
        
        """).strip()

        Path(slug).with_suffix('.md').write_text(t)





@main.group(help='manage java modules repos and websites')
def java():
    pass


@java.command(name='web', help='Update a level website')
@click.option('-l', '--level', help="Name of the level to generate a lesson plan for")
@click.option('-o', '--org', default='League-Java', help="Org or owner of the repo")
def jweb(level: str, org: str):
    from plumbum import local
    from plumbum.cmd import yarn

    level = level.title()

    new_vuepress(level, dest_org=org)

    bd = build_dir(level)

    clone_or_pull_repo(org, level, bd )

    ld = bd / 'docs'

    assert ld.exists(), f"Vuepress dir '{ld}' does not exist"

    if not (ld / 'docs' / 'node_modules').exists():
        with local.cwd(ld):
            logger.info("Installing vuepress in " + str(ld))
            yarn('install')



@java.command(name='push', help='Push modules to repos. Depends on meta.yaml, so make sure it is updated first')
@click.option('-l', '--level', default=None, help="Push all modules from this level")
@click.option('-m', '--module', default = None, help="With --level, push use this module")
@click.option('-o', '--org', default='League-Java', help="Org or owner of the repo")
def jpush(level, module, org="League-Java"):

    meta = yaml.safe_load(Path(get_repo_root() / 'meta.yaml').read_text())

    assert not( module and not level), "If module is specified, must also specify level"

    level_glob = level if level else '*'
    mod_glob = module if module and level else '*'

    mods = []
    for f in get_repo_root().glob(f'levels/{level_glob}/{mod_glob}'):
        if f.is_dir():
            mods.append(f)

    logger.info(f"Pushing {len(mods)} modules to {org}")

    for m in mods:
        create_repo(m, org, build_dir)

@java.command(name='meta', help='Regenerate meta.yaml')
@click.option('-l', '--level_dir', default='levels', help="Root directory to levels")
def jmeta(level_dir='levels'):
    update_meta(get_repo_root(), level_dir)


@java.command(name='serve', help='Development server for a level website')
@click.option('-l', '--level', help="Name of the level to serve")
@click.pass_context
def jserve(ctx, level):
    r = get_repo_root()
    docs_path = build_dir(level) / 'docs'

    ctx.invoke(serve, docs_path=docs_path)


@java.command(name='build', help='Build the lesson website for a level')
@click.option('-l', '--level', help="Name of the level to serve")
@click.option('-Y', '--yarn-build', is_flag=True, default=False, help='Also run Yarn Build')
@click.option('-w', '--watch', is_flag=True, default=False, help='Rebuild when source files change')
@click.pass_context
def jbuild(ctx, level, yarn_build=False, watch=False):
    r = get_repo_root()

    level = level.title()

    web_root = build_dir(level)
    docs_path = web_root / 'docs'
    lesson_path = web_root / 'lessons'

    meta = yaml.safe_load(Path(r / 'meta.yaml').read_text())
    meta = meta[level]

    make_lessons(r, web_root, meta)

    ctx.invoke(build, lesson_path=lesson_path, docs_path=docs_path,
               url_base=level, yarn_build=yarn_build, watch=watch)


@java.command(name='deploy', help="Deploy the website to Github Pages")
@click.option('-l', '--level', help="Name of the level to serve")
@click.pass_context
def jdeploy(ctx, level):
    r = get_repo_root()
    docs_path = build_dir(level) / 'docs'

    logger.info("Deploying " + str(docs_path))
    ctx.invoke(deploy, docs_path=docs_path)


if __name__ == '__main__':
    main_entry()

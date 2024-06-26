import logging

import yaml

from .git import create_repo
from .html import _proc_html
from .util import *
from .walk import *

logger = logging.getLogger('lesson-builder')


def update_modules(repo_root, levels_root):
    """Update all of the module directories with settings files, scripts, etc. """

    for dir_ in walk_modules(levels_root):
        make_dirs(dir_)
        write_classpath(dir_)
        write_settings(dir_)
        write_gitignore(dir_)
        write_launch(dir_)
        copy_devcontainer(repo_root, dir_)
        # copy_scripts(dir_)
        disable_eclipse(dir_)


def push(repo_root, root, org, build_dir):
    """Upload the module in the current dir to Github"""

    for dir_ in walk_modules(root):
        create_repo(dir_, org, build_dir)
        # make_repo_template(dir_)


def update_meta(repo_root, level_root):
    """Create the .meta files for the assignments, while hold information
    used in creating README, images, and assigment pages."""

    import yaml

    asgn_metas = []

    # Read the meta for the assignments. This will
    # get READMEs for the assignments and put it in to the
    # 'text' key in the metadata
    for l in walk_assignments(Path(level_root)):
        # java = list(l.glob('*.java'))
        # pde = list(l.glob('*.pde'))
        # web = (l / '.web').exists()

        r = process_dir(repo_root, level_root, l)

        if r:
            (l / '.meta').write_text(yaml.dump(r, indent=2))
            asgn_metas.append(r)
        else:
            logger.debug("No meta " + str(l))

    metas = compile_meta(asgn_metas)

    # Add in readmes for levels and modules
    ld = Path(level_root).absolute()

    for p in ld.glob('**/README.md'):
        if '/src/' in str(p) or '/bin/' in str(p):
            continue

        l, m = get_lm(p)
        if l and not m:
            metas[l]['_readme'] = p.read_text()
        elif l and m:
            metas[l][m]['_readme'] = p.read_text()
        else:
            print(f"Could not find level or module for {p}")


    # Readmes for lessons, which are the parent directories of the
    # assignments
    for p in ld.glob('**/README.md'):
        if '/src/' not in str(p) or '/bin/' in str(p):
            continue

        l, m, ls, a = get_lmla(p)
        if a == 'README.md':
            try:
                metas[l][m][ls.strip('_')]['_readme'] = p.read_text()
            except KeyError:
                assert '99' in ls, f"Could not find {l} {m} {ls} in metas"
                # This happens for 99_extras, which don't have any metadata
                #print(metas[l][m].keys(), f"Could not find {l} {m} {ls} in metas")
                pass


    # Create missing readmes
    for i, (mk, mv) in enumerate(sorted(metas.items())):

        if not '_readme' in mv:
            mv['_readme'] = f"# {mk}\n\n"

    (repo_root / 'meta.yaml').write_text(yaml.dump(metas, indent=2))


def make_readme(root):
    """Process the web pages in the .web directories
    HISTORIC: Now that the readmes have been created, they should be used
    instead of the text in the .meta files."""
    root = Path(root)

    for f in root.glob("**/.meta"):
        m = yaml.load(f.read_text(), Loader=yaml.SafeLoader)

        adir = f.parent
        images_dir = adir / 'images'

        images_dir.mkdir(parents=True, exist_ok=True)

        for r in m['resources']:
            r = Path(r)
            shutil.copy(r, images_dir / r.name)

        (f.parent / 'README.md').write_text(m['text'])


def fetch_web(root):
    """Walk the levels looking for html files and download the assets
    HISTORIC, probably not needed anymore"""
    root = Path(root)

    for f in root.glob("**/*.html"):
        if '/bin/' in str(f):
            continue

        if '/.web/' in str(f):
            continue

        _proc_html(f)

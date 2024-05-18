from pathlib import Path
from lesson_builder.config import resource_extensions

def walk_modules(root):
    root = Path(root)

    if root.name.startswith("Module"):
        yield root

    for dir_ in root.glob("**/*"):
        if dir_.name.startswith("Module"):
            yield dir_


def walk_lessons(root):
    for m in walk_modules(root):
        src = m / 'src'
        if src.exists():
            for a in src.iterdir():
                if a.is_dir():
                    yield a


def get_lm(dir_=None):
    if dir_ is None:
        p = Path('.')
    else:
        p = Path(dir_)

    parts = str(p.absolute()).split('/')

    l = None
    m = None

    for i, part in enumerate(parts):
        if part.startswith("Level"):
            l = part
        if part.startswith("Module"):
            m = part

    assert l is None or l.startswith("Level")
    assert m is None or m.startswith("Module")

    return l, m


def get_lmla(dir_=None):
    """Get level, module, lesson, assignment from a directory"""
    if dir_ is None:
        p = Path('.')
    else:
        p = Path(dir_)

    p = str(p.absolute())

    if not '/src/' in p:
        return None, None, None, None

    # The lesson is the first directory after 'src',
    # and the assignment is the directory after the lesson.

    lm, la = p.split("src")

    lm_parts = lm.strip("/").split('/')
    la_parts = la.strip("/").split('/')

    l = lm_parts[-2]
    m = lm_parts[-1]

    ls = None
    a = None

    try:
        ls = la_parts.pop(0);
    except IndexError:
        print("   ", dir_)
        pass

    try:
        a = la_parts.pop(0)
    except IndexError:
        pass

    return l, m, ls, a


def find_leaf_directories(root_dir):
    from os import walk

    root_path = Path(root_dir)
    leaf_directories = []  # List to hold the Path objects of leaf directories

    for dirpath, dirnames, filenames in walk(root_path):
        dirpath = Path(dirpath)

        dirnames = [e for e in dirnames if e not in ('.web', 'lib', 'league_token')]

        if not dirnames and dirpath.name not in ('.web', 'lib', 'league_token') \
                and '/src/' in str(dirpath):
            leaf_directories.append(Path(dirpath))

    return leaf_directories


def remove_leading_numbers(s):
    """Strip '_' and leading numbers from a string"""
    s = s.strip('_')

    while s[0].isdigit():
        s = s[1:]

    return s

def process_dir(repo_root, root, f):
    from .html import html_to_markdown

    if f.name in ('.web', 'lib', 'league_token', 'tests'):
        f = f.parent

    try:
        l, m, ls, a = get_lmla(f)
    except Exception as e:
        print("ERROR (lmla) ", f, e)
        return None

    if a is None and ls is None:
        # Module level
        # print("No assignment ", f)
        return None

    elif a is None and ls is not None:
        # missing one level of less / assignment
        ls = ls.strip('_')
        a = ls
        assign = ls
    else:
        assign = ls.strip('_')

    ls = ls.strip('_')

    title = assign.replace('_', ' ').title()

    web_dir = (f / '.web')

    readme = f / 'README.md'

    if readme.exists():
        md = readme.read_text()
    else:
        idx = web_dir / 'index.html'
        if idx.exists():
            md = html_to_markdown(idx)
        else:
            md = f"# {title}\n\n"

    r = {
        'title': title,
        'dir': str(f),
        'opath': str(f),
        'level': l,
        'module': m,
        'lesson': ls,
        'oassignment': a.strip('_'),
        'assignment': assign,
        'resources': [],
        'text': md
    }

    resources = []
    if web_dir.exists():
        for e in web_dir.iterdir():
            if e.is_file() and e.suffix in resource_extensions:
                resources.append(str(e))

    r['resources'] = resources

    return r


def walk_assignments(root):
    adirs = set()

    for f in root.glob('**/*'):
        p = f.parent

        if p.name in ('.web', 'lib', 'league_token', 'tests', 'bin'):
            continue

        java = list(p.glob('*.java'))
        pdf = list(p.glob('*.pdf'))

        web = (p / '.web').exists()

        if len(java) > 0 or len(pdf) > 0 or web:
            adirs.add(p)

    return list(sorted(adirs))

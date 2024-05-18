# Support for building level websites.

from pathlib import Path

import frontmatter
import yaml

from .util import logger
from .render import javaref, forkrepo, reporef

def add_after_h1(markdown_text, string_to_add):
    lines = markdown_text.split('\n')

    for i, line in enumerate(lines):
        if line.startswith('# '):
            lines.insert(i + 1, string_to_add + '\n')
            break
    # Join the lines back into a single string
    o = '\n'.join(lines)

    return o


def indent_headings(meta, t):
    lines = []

    found_first = False

    for l in t.splitlines():
        if l.startswith('#'):
            l = "#" + l  # Bump all the headings up one level.

            if not found_first:
                l += "\n\n{{ javaref(fm_level, fm_module,fm_lesson,fm_assignment, fm_dir) }}\n"

            found_first = True

        lines.append(l)

    return '\n'.join(lines)


def add_javaref(meta, t):
    lines = []

    found_first = False

    for l in t.splitlines():
        if l.startswith('#'):

            if not found_first:
                l += "\n\n{{ javaref(fm_level, fm_module,fm_lesson,fm_assignment, fm_dir) }}\n"

            found_first = True

        lines.append(l)

    return '\n'.join(lines)


def make_text(lv):
    first = dict(**lv[0])

    if len(lv) == 1:
        o = add_javaref(first, first['text'])
    else:
        title = first['lesson'].replace('_', ' ').title()

        o = f"# {title}\n\n"

        for a in lv:
            o += indent_headings(a, a['text'])

    # Find all html images tags  of the form './images/<name>'
    # and replace the source with './<name>'

    o = o.replace('./images/', './')

    del first['text']
    del first['resources']

    o = f"""---\n{yaml.dump(first)}---\n{o}"""

    #o = add_after_h1(o, '\n{{ forkrepo(fm_level, fm_module) }}\n\n{{ reporef(fm_level, fm_module) }}\n\n')

    return o


def copy_resources(dir_, lv):
    for v in lv:

        if not 'resources' in v:
            logger.debug(f"No resources in {v['assignment']}")
            continue

        for r in v['resources']:
            r = Path(r)

            if r.exists():
                r = r.resolve()
                if r.is_file():
                    d = dir_ / r.name
                    d.parent.mkdir(parents=True, exist_ok=True)
                    d.write_bytes(r.read_bytes())

                else:
                    logger.debug(f"Resource {r} is not a file.")
            else:
                logger.dubug(f"Resource {r} does not exist.")


def make_lessons(level, repo_root, web_root, meta):
    """Build the lessons directory for a java level"""

    ld = web_root / 'lessons'

    ld.mkdir(parents=True, exist_ok=True)

    lessons = {}

    # Meta should already be restricted to one level,
    # so we can just iterate over the modules and lessons.

    n_modules = 0
    n_lessons = 0
    first_key = None

    for i, (mk, mv) in enumerate(sorted(meta.items())):

        if i == 0:
            first_key = mk

        # The level readme, which goes on the main page of the website
        if mk == '_readme':
            # strip the first level one heading from mv
            t = ''
            for l in mv.strip().splitlines():
                if l.startswith('# '):
                    continue
                t += l + '\n'

            f = ld / 'index.md'
            f.parent.mkdir(parents=True, exist_ok=True)

            if f.exists():
                post = frontmatter.loads(f.read_text())
                fm = post.metadata
            else:

                fm = {
                    "actionText": "Get Started!",
                    "heroImage": "/assets/word-logo.png",
                    "home": True,
                    "tagline": "Igniting Young Minds Through Programming"
                }

            fm["actionLink"] = f"/lessons/{first_key}/"

            # Create a new frontmatter post
            post = frontmatter.Post(t, **fm)

            # Output the combined content with frontmatter
            t = frontmatter.dumps(post)

            f.write_text(t)

            continue

        n_modules += 1

        if mk not in lessons:
            lessons[mk] = {
                'title': mk,
                'assignments': []
            }

        readme = mv.pop('_readme', None)
        for lk, lv in sorted(mv.items()):

            n_lessons += 1

            ltitle = (' '.join(lk.split('_')[1:])).title()

            dir_ = ld / mk / lk

            dir_.mkdir(parents=True, exist_ok=True)

            text = make_text(lv)

            (dir_ / 'index.md').write_text(text)

            fm = dict(frontmatter.loads(text))

            copy_resources(dir_, lv)

            (dir_ / '_assignment.yaml').write_text(yaml.dump(fm))

            lessons[mk]['assignments'].append(str(dir_.relative_to(ld)))
            lessons[mk]['assignments'] = list(sorted(lessons[mk]['assignments']))


        if not readme:
            readme = "# " + mk.replace('_', ' ').title() + "\n\n"


        # Write the module readme text, the intro to the module.
        dir_ = ld / mk / 'index.md'
        dir_.parent.mkdir(parents=True, exist_ok=True)

        readme = add_after_h1(readme, '\n{{ forkrepo(fm_level, fm_module) }}\n\n{{ reporef(fm_level, fm_module) }}\n\n')

        fm = {
            "template": "readme.md",
            "level": level,
            "module": mk
        }

        readme = frontmatter.dumps(frontmatter.Post(readme, **fm))

        dir_.write_text(readme)



    lp = yaml.safe_load((ld / 'lesson-plan.yaml').read_text())

    lp['lessons'] = lessons

    logger.info(f"Built {n_modules} modules and {n_lessons} lessons in {web_root}")

    (ld / 'lesson-plan.yaml').write_text(yaml.dump(lp, sort_keys=False))

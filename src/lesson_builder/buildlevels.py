# Support for building level websites.

from pathlib import Path

import yaml


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
                l += "\n\n{{ javaref(fm_level, fm_level,fm_lesson,fm_assignment, fm_dir) }}\n"

            found_first = True

        lines.append(l)

    return '\n'.join(lines)

def make_text(lv):

    first = lv[0]

    if len(lv) == 1:
        o = indent_headings(first, first['text'])
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

    o = add_after_h1(o, '\n\n{{ reporef(fm_level, fm_module) }}\n{{ forkrepo(fm_level, fm_module) }}\n')

    return o


def copy_resources(dir_, lv):
    for v in lv:
        if not 'resources' in v:
            continue

        for r in v['resources']:
            r = Path(r)
            if r.exists():
                r = r.resolve()
                if r.is_file():
                    d = dir_ / r.name
                    d.parent.mkdir(parents=True, exist_ok=True)
                    d.write_bytes(r.read_bytes())


def make_lessons(repo_root, web_root,  meta):
    """Build the lessons directory for a java level"""



    ld = web_root / 'lessons'

    ld.mkdir(parents=True, exist_ok=True)

    lessons = {}

    lp = {
        'title': 'Java Levels',
        'description': 'All of the Java Levels',
        'pages': [],
        'resources': [],
        'sidebar': [],
        'lessons': None
    }

    for mk, mv in sorted(meta.items()):

        if mk.startswith('_'):

            continue

        if mk not in lessons:
            lessons[mk] = {
                'title': mk,
                'assignments': []
            }

        for lk, lv in sorted(mv.items()):

            if lk.startswith('_'):
                dir_ = ld / mk / 'index.html'

                dir_.parent.mkdir(parents=True, exist_ok=True)
                dir_.write_text(lv)
                continue

            ltitle = (' '.join(lk.split('_')[1:])).title()
            print(mk, ltitle, len(lv))

            dir_ = ld / mk / lk

            dir_.mkdir(parents=True, exist_ok=True)

            text = make_text(lv)

            (dir_ / 'index.md').write_text(text)

            a = {
                'level': lk,
                'module': mk,
                'lesson': lk,
                'title': ltitle,
                'description': ''
            }

            copy_resources(dir_, lv)

            (dir_ / '_assignment.yaml').write_text(yaml.dump(a))

            lessons[mk]['assignments'].append(str(dir_.relative_to(ld)))
            lessons[mk]['assignments'] = list(sorted(lessons[mk]['assignments']))

    lp['lessons'] = lessons

    (ld / 'lesson-plan.yaml').write_text(yaml.safe_dump(lp))

""" Object structure for the lesson plan, the lessons and assignments.
Iterates through the lesson plan and writes the lessons and assignments to the
file system.
"""
import logging
import shutil
from dataclasses import dataclass
from pathlib import Path
from textwrap import dedent
import frontmatter
import yaml

from .render import render

logger = logging.getLogger(__name__)

indent = '    '

example_config = 'https://github.com/league-curriculum/Visual-Python/blob/main/assignments/config.yml'


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


@dataclass
class ResourceWrite:
    source: Path | str | bytes
    dest: Path

    @property
    def is_render(self):
        return isinstance(self.source, dict)

    def render(self):
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
            src = str(self.source)

        elif isinstance(self.source, str):
            src = f"<{len(self.source)} bytes>"
        elif isinstance(self.source, dict):
            src = f"<Render {self.source['working_directory'].name}>"

        dst = str(self.dest)

        return f"{src} -> {dst}"


def get_assignment(path):
    """Read an assignment and construct a dict of the important information"""

    path = Path(path)
    meta_path = path / '_assignment.yaml'

    if not meta_path.exists():
        logger.warning(f"No _assignment.yaml meta file found in {path}")
        return {
            'sources': [],
            'texts': {},
            'resources': []
        }

    meta = yaml.safe_load(meta_path.read_text())
    meta['source_dir'] = path
    meta['texts'] = {}
    meta['resources'] = []
    meta['sources'] = []

    for f in path.glob('*.py'):
        meta['sources'].append(f)

    for f in path.glob('*.md'):
        meta['texts'][f.stem] = f

    for f in list(path.glob('*.png')) + list(path.glob('*.gif')):
        meta['resources'].append(f)

    return meta


class Assignment:
    def __init__(self, lesson: "Lesson", assignment_dir):
        self.lesson = lesson
        self.ass_dir = Path(assignment_dir)

        if not self.ass_dir.exists():
            raise FileNotFoundError(f'Assignment directory nonexistant: ', assignment_dir)
        self.ass_data = get_assignment(self.ass_dir)

    @property
    def title(self):
        try:
            return self.ass_data['title']
        except KeyError:
            logger.warning(f'Did not get a title from assignment data, directory {self.ass_dir}\n')
            return "<No Title>"

    @property
    def name(self):
        return self.ass_data['source_dir'].name

    @property
    def src_dir(self):
        """Source directory for the assignment"""
        return self.ass_dir

    @property
    def dest_dir(self):
        return self.lesson.dest_dir / self.name

    def render(self):

        ad = self.ass_data

        for text_name in ('trinket', 'index'):
            if text_name in ad['texts']:
                text = ad['texts'][text_name].read_text()
                break
        else:
            logger.warning(f"No text content for {self.src_dir}")
            return None

        # We are turning a dict here so it can be rendered later. The dict is the
        # argument list for render()
        md = dict(template_name='assignment.md',
                  frontmatter={'title': ad['title']},
                  title=ad['title'],
                  working_directory=self.dest_dir,
                  content=text)

        return ResourceWrite(md, self.dest_dir / 'index.md')

    def collect_writes(self):

        res = []

        ad = self.ass_data

        # Copy the source files
        for source in ad['sources']:
            res.append(ResourceWrite(source, self.dest_dir / source.name))

        # Copy other resources
        for f in list(ad['resources']) + list(ad['sources']):
            f = Path(f)
            res.append(ResourceWrite(f, self.dest_dir / f.name))

        r = self.render()
        if r:
            res.append(r)
        else:
            logger.warning(f"Render returned nothing for {self.src_dir}")

        return res

    @property
    def sidebar_entry(self):

        return {
            'path': f'/lessons/{self.lesson.name}/{self.name}/',
            'title': self.title
        }

    def __str__(self):
        return self.title or '<No Title>'


class Lesson:
    """A Lesson is a collection data from the lesson plan. It may also
    have a directory, but may not. If it does, it will be a sub-directory of the
    containing directory of the lesson plan """

    def __init__(self, lesson_plan: "LessonPlan", lesson_data):
        self.lesson_plan = lesson_plan
        self.ld = lesson_data

    @property
    def name(self):
        return self.ld['name']

    @property
    def src_dir(self):
        d = self.lesson_plan.less_plan_dir / self.name
        if not d.exists():
            return None
        return d

    @property
    def has_dir(self):
        return self.src_dir is not None and self.src_dir.is_dir()

    @property
    def dest_dir(self):
        return self.lesson_plan.less_output_dir / self.name

    @property
    def lesson_text_path(self):

        lpt_base = self.lesson_plan.less_plan_dir / self.name

        lt_path_file = lpt_base.with_suffix('.md')
        lt_path_index = self.src_dir / 'index.md' if self.has_dir else None

        if 'text' in self.ld:
            #  the text field is the name of the file, in the lesson plan dir
            lt_path = self.lesson_plan.less_plan_dir / self.ld['text']
        elif lt_path_file.exists():
            lt_path = lt_path_file
        elif self.has_dir and lt_path_index is not None and lt_path_index.exists():
            lt_path = lt_path_index
        else:
            raise FileNotFoundError(dedent(f"""
            No lesson text file for {self.name}. Do one of:
              * Add 'text: <filename>' to the lesson plan 
              * Create a '{lpt_base}' directory with an index.md file.
              * Create a '{lpt_base}.md' file
              """).strip())

        return lt_path

    @property
    def lesson_text(self):
        try:
            return self.lesson_text_path.read_text()
        except FileNotFoundError:
            raise FileNotFoundError(f"No lesson file for {self.lesson_text_path}")

    @property
    def title(self):
        fm = frontmatter.loads(self.lesson_text)
        try:
            return fm['title']
        except KeyError:
            title = get_first_h1_heading(self.lesson_text_path)

            if not title:
                raise KeyError(f'Assignment {self.name} does not have a title in frontmatter not H2 heading')
            else:
                return title

    def collect_writes(self):
        """Write the lesson to the root directory

        Args:
            root (Path): The root directory of lessons in the vuepress site
        """

        res = []

        if self.lesson_text_path.exists():
            res.append(ResourceWrite(self.lesson_text_path, self.dest_dir / 'index.md'))

        # Copy images and other assets
        for resource in self.ld.get('resources', []):
            res.append(ResourceWrite(self.lesson_plan.assets_src_dir / resource, self.dest_dir / resource))

        for a in self.assignments:
            res.extend(a.collect_writes())

        return res

    @property
    def sidebar_entry(self):
        """
        - collapsable: false
          title: lesson2
          children:
            - path: /lessons/lesson2/flaming-ninja-star/
              title: Flaming Ninja Star
            - path: /lessons/lesson2/turtle-spiral/
              title: Turtle Spiral

        """

        return {
            'collapsable': False,
            'title': self.title,
            'path': f'/lessons/{self.name}/',
            'children': [c.sidebar_entry for c in self.assignments]
        }

    @property
    def assignments(self):
        for a in self.ld['assignments']:

            abs_dir = self.lesson_plan.asgn_dir / a

            if not abs_dir.exists():
                raise FileNotFoundError(f'Assignment {a} not found in assignment dir {abs_dir}')

            yield Assignment(self, abs_dir)

    def __str__(self):
        return f"Lesson: {self.title} {self.name} dir={self.src_dir}"


class LessonPlan:

    def __init__(self, less_plan_dir, vue_doc_dir, asgn_dir=None,
                 less_subdir='lessons'):
        """ Create a new lesson plan

        Args:
            less_plan_dir: Root dir for the lesson plan and other files, or a path to the lesson plan
            vue_doc_dir: The source dir for vuepress files, usually 'docs'
            asgn_dir: The directory for the assignments
            less_subdir: subdir in web_src_dir for generated lesson files.
        """

        if Path(less_plan_dir).is_file():
            self.less_plan_dir = Path(less_plan_dir).parent
            self.lesson_plan_file = Path(less_plan_dir)

        else:
            self.less_plan_dir = Path(less_plan_dir)
            self.lesson_plan_file = self.less_plan_dir / 'lesson-plan.yaml'

        self.lesson_plan = yaml.safe_load(self.lesson_plan_file.read_text())
        self.vue_doc_dir = Path(vue_doc_dir)
        self.web_src_dir = self.vue_doc_dir / 'src'
        self.less_output_dir = self.web_src_dir / less_subdir  # Where we write lesson outputs

        self.assets_src_dir = self.less_plan_dir / 'assets'

        self.asgn_dir = asgn_dir if asgn_dir is not None else self.less_plan_dir

    @property
    def lessons(self):
        for lesson_key, lesson in self.lesson_plan['lessons'].items():
            lesson['name'] = lesson_key
            yield Lesson(self, lesson)

    def update_config(self, basedir=None):
        """Generate the config file for viuepress"""

        lp = self.lesson_plan

        # Read the config from the lesson plan
        config_file = self.less_plan_dir / 'config.yml'

        if not config_file.exists():
            raise FileNotFoundError(
                "No config file found in lesson plan. 'config.yml' is required "
                " in the lesson plan directory.\n ( expected it at"
                "_You can probably just copy this one {example_config}: " +
                example_config)

        config = yaml.safe_load(config_file.read_text())

        if not config:
            raise ValueError(f"Config file {config_file} is empty")

        config['title'] = lp['title']
        config['description'] = lp['description']

        if basedir:
            config['base'] = '/' + basedir.strip('/') + '/'

        # config output file for vuepress
        config_file = self.web_src_dir / '.vuepress/config.yml'

        config['themeConfig']['sidebar'] = self.make_sidebar()

        logger.info(f'Writing config to {config_file}')
        config_file.write_text(yaml.dump(config))

        # Remove the old config.js file
        js_config = self.web_src_dir / '.vuepress/config.js'
        if js_config.exists():
            js_config.unlink()

    def collect_writes(self):
        """Collect all of the files to be written"""

        res = []

        # Copy pages from the root of the lesson dir to the website src dir
        for page in self.lesson_plan['pages']:
            res.append(ResourceWrite(self.less_plan_dir / page, self.web_src_dir / page))

        assets_dir = self.web_src_dir / '.vuepress/public/assets'

        for resource in self.lesson_plan['resources']:
            res_file = self.less_plan_dir / 'assets' / resource
            dest_file = assets_dir / resource

            res.append(ResourceWrite(res_file, dest_file))

        for lesson in self.lessons:
            res.extend(lesson.collect_writes())

        return res

    def write_dir(self):
        """Write the lesson plan to the root directory

        """

        # Write all of the files first
        for r in self.collect_writes():
            if not r.is_render:
                logger.debug(f'Writing {r}')
                r.write()

        # Then do the renders
        for r in self.collect_writes():
            if r.is_render:
                logger.debug(f'Rendering {r}')
                r.render()

    def build(self, root_dir: Path = None, url_base_dir=None):
        """Write the lesson plan to the root directory

        Args:
            root_dir (Path): The root directory to write the lesson to
            url_base_dir (str): The base directory for the URL
        """

        root_dir = self.less_output_dir if root_dir is None else root_dir

        logger.info(f'Writing lesson plan to {root_dir}')

        self.write_dir()

        self.update_config(url_base_dir)

    def make_sidebar(self):

        return (self.lesson_plan['sidebar'] + [l.sidebar_entry for l in self.lessons])

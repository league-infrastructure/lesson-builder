""" Object structure for the lesson plan, the lessons and assignments.
Iterates through the lesson plan and writes the lessons and assignments to the
file system.
"""
import logging
from pathlib import Path
from textwrap import dedent

import frontmatter

from .assignment import Assignment
from .util import ResourceWrite, get_first_h1_heading

logger = logging.getLogger('lesson-builder')

indent = '    '


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
        elif 'title' in self.ld:
            # No text is expected
            lt_path = None
        else:
            raise FileNotFoundError(dedent(f"""
            No lesson text file for {self.name}. Do one of:
              * Add 'text: <filename>' to the lesson plan 
              * Create a '{lpt_base}' directory with an index.md file.
              * Create a '{lpt_base}.md' file
              * Define a title in the lesson in the lesson-plan
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

        if 'title' in self.ld:
            return self.ld['title']

        fm = frontmatter.loads(self.lesson_text)
        try:
            return fm['title']
        except KeyError:

            title = get_first_h1_heading(self.lesson_text_path)

            if not title:
                raise KeyError(f'Assignment {self.name} does not have a title in frontmatter nor H2 heading')
            else:
                return title

    def collect_writes(self):
        """Write the lesson to the root directory

        Args:
            root (Path): The root directory of lessons in the vuepress site
        """

        res = []

        if self.lesson_text_path is not None and self.lesson_text_path.exists():
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

        assert self.title

        d = {
            'collapsable': False,
            'title': self.title,
            'children': [c.sidebar_entry for c in self.assignments]
        }
        if self.lesson_text_path is not None:
            d['path'] = f'/lessons/{self.name}/'

        return d

    @property
    def assignments(self):
        for a in self.ld.get('assignments',[]):

            abs_dir = self.lesson_plan.asgn_dir / a

            if not abs_dir.exists():
                raise FileNotFoundError(f'Assignment {a} not found in assignment dir {abs_dir}')

            yield Assignment(self, abs_dir)

    def __str__(self):
        return f"Lesson: {self.title} {self.name} dir={self.src_dir}"

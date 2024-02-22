from pathlib import Path

import yaml

from .lesson import Lesson

from .config import example_config
from .util import ResourceWrite

import logging
logger = logging.getLogger('lesson-builder')

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

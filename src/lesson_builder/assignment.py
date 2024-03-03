from pathlib import Path


from .trinket import generate_trinket_iframe
from .util import ResourceWrite, get_first_h1_heading
import yaml
import logging
import frontmatter
logger = logging.getLogger('lesson-builder')


def get_resource_references(dir_, text):

    # get the files names for images references in markdown style
    # images, ![alt text](path)
    import re
    md_images = re.findall(r'!\[.*\]\((.*)\)', text)

    # get the files names for images references in html style
    # images, <img src="path" alt="alt text">
    html_images = re.findall(r'<img src="(.*)"', text)

    r = md_images + html_images

    # Make the paths absolute to the assignment dir
    return [ (dir_ /f).absolute() for f in r]

    return

def get_assignment(path):
    """Read an assignment and construct a dict of the important information"""

    path = Path(path)

    def prep_meta(meta):
        meta['texts'] = {}
        meta['resources'] = []
        meta['sources'] = []

    if path.is_file():
        text = path.read_text()

        meta = frontmatter.loads(text)
        if not 'title' in meta:
            meta['title'] = get_first_h1_heading(path)

        meta['source_dir'] = None
        meta['name'] = path.stem
        prep_meta(meta)

        meta['texts']['trinket'] = path

        meta['resources'] = get_resource_references(path.parent, text)

    elif path.is_dir():
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
        meta['name'] = path.name
        prep_meta(meta)

        for f in path.glob('*.py'):
            meta['sources'].append(f)

        for f in path.glob('*.md'):
            meta['texts'][f.stem] = f

        for f in list(path.glob('*')):
            if f.suffix  in ('.png', '.jpg', '.gif'):
                meta['resources'].append(f)

    return meta


class Assignment:
    def __init__(self, lesson: "Lesson", path):
        self.lesson = lesson
        self.path = Path(path)

        if not self.path.exists():
            raise FileNotFoundError(f'Assignment directory nonexistant: ', path)

        self.ass_data = get_assignment(self.path)

    @property
    def title(self):
        try:
            return self.ass_data['title']
        except KeyError:
            logger.warning(f'Did not get a title from assignment data, directory {self.path}\n')
            return "<No Title>"

    @property
    def name(self):
        return self.ass_data['name']

    @property
    def src_dir(self):
        """Source directory for the assignment"""
        return self.path

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
            logger.warning(f"No text content for {self.name} ({ad['texts']})")
            return None

        from .trinket import  extract_python

        def replace_f(code, height):
            return generate_trinket_iframe(code, height=str(height), width='100%')

        # Convert "```python.run" lines, which are not
        # handled by Markdown.
        modified_text, code = extract_python(text,  replacement_f=replace_f)

        # We are turning a dict here so it can be rendered later. The dict is the
        # argument list for render()
        md = dict(template_name='assignment.md',
                  frontmatter={'title': ad['title']},
                  title=ad['title'],
                  working_directory=self.dest_dir,
                  content=modified_text)

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
            logger.warning(f"Render returned nothing for {self.name}")

        return res

    @property
    def sidebar_entry(self):

        return {
            'path': f'/lessons/{self.lesson.name}/{self.name}/',
            'title': self.title
        }

    def __str__(self):
        return self.title or '<No Title>'

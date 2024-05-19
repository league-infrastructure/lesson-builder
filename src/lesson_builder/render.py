import re
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader
import frontmatter
import lesson_builder.templates as tmpl
from lesson_builder.config import level_module_repo_src_tmpl, level_module_repo_tmpl
from .trinket import read_code, trinket, goal_image
from textwrap import dedent

def strip_html(text):
    return re.sub('<.*?>', '', text) if text else ''


def dict_to_yaml(d):
    if not d:
        return ''
    return yaml.dump(d, allow_unicode=True)

def display_button(text, color, url,icon_image):

    return dedent(f"""
    <div style="background-color: {color}; padding: 10px 24px; margin-bottom:10px; cursor: pointer; width: 200px;">
    <a href="{url}" target="_blank" 
    style="text-decoration: none; color: white; font-size: 14pt; display: flex; align-items: center; gap: 10px;">
    <img :src="$withBase('/assets/{icon_image}')" alt="{text}" style="width:30px; vertical-align: middle;">
    {text}
    </a>
    </div>""").strip()

def button_link(text, color, url, icon_image):
    """Display a colored box with a link to a URL."""
    return dedent(f"""
    <span style="background-color: {color}; padding: 10px 24px; margin-bottom:10px; margin-right: 10px;">
    <a href="{url}" target="_blank"  style=" color: white; font-size: 14pt; align-items: center; gap: 10px;">
    <img :src="$withBase('/assets/{icon_image}')" alt="{text}" style="width:20px; vertical-align: middle;">
    {text}
    </a>
    </span>""").strip()

def simple_link(text, color, url,icon_image):
    """Display a sikmple link with an icon."""
    return (f"<a href=\"{url}\" target=\"_blank\"><img :src=\"$withBase('/assets/{icon_image}')\" alt=\"{text}\" "
            f"style=\"width:20px; vertical-align: middle;\"> {text}</a>")

def javaref(level, module, lesson, asgn, dir):
    """A view source button, which coes on each lesson"""
    p = dir.split('/src/')[-1].strip('/')
    dir_url = level_module_repo_src_tmpl.format(level=level, module=module, path=p)

    return simple_link(f"View Source", "gray", dir_url, "github-mark.png")

def reporef(level, module):
    repo_url = level_module_repo_tmpl.format(level=level, module=module)

    return button_link(f"View {level}-{module}", "blue", repo_url, "github-mark-white.png")

def forkrepo(level, module):
    fork_url = level_module_repo_tmpl.format(level=level, module=module) + '/fork'

    return button_link(f"Fork {level}-{module}", "green", fork_url, "github-mark-white.png")

def strip_frontmatter(markdown_text):
    """
    Strips the frontmatter from a markdown post delimited by '---'.

    Parameters:
    markdown_text (str): The markdown text including frontmatter.

    Returns:
    str: The markdown text without the frontmatter.
    """
    # Split the text at '---'
    parts = markdown_text.split('---', 2)

    # If there are at least three parts, frontmatter is present and removed
    if len(parts) >= 3:
        # Return the content without frontmatter
        return parts[2].strip()
    else:
        # Return the original text if no frontmatter is found
        return markdown_text


def render(template_name, *args, **kwargs):
    """Render a Jinja2 template"""

    tmpl_dir = Path(tmpl.__file__).parent

    env = Environment(loader=FileSystemLoader(tmpl_dir))
    env.filters['strip_html'] = strip_html
    env.globals['trinket'] = trinket
    env.globals['goal_image'] = goal_image
    env.globals['javaref'] = javaref
    env.globals['forkrepo'] = forkrepo
    env.globals['reporef'] = reporef
    env.globals['read_code'] = read_code
    env.filters['yaml'] = dict_to_yaml

    if 'content' in kwargs:

        fm = frontmatter.loads(kwargs['content'])
        kwargs['content'] = fm.content

        for k, v in fm.metadata.items():
            kwargs["fm_"+k] = v

        try:
            t = env.from_string(kwargs['content'])
        except Exception as e:
            print(f"======\n\nError creating template from content")
            print(f"content: {kwargs['content']}")
            raise

        try:
            kwargs['content'] = t.render(*args, **kwargs)
        except Exception as e:
            print(f"Error rendering content: {e}")
            print(f"args: {args}")
            print(f"kwargs: {kwargs}")
            raise
    else:
        print("No content!!!!", kwargs.keys())



    template = env.get_template(template_name)

    return template.render(*args, **kwargs)

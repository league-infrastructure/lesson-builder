import html
import re
from textwrap import dedent

from bs4 import BeautifulSoup, NavigableString


def html_list_to_markdown(html_list):
    """Convert an HTML list (ul or ol) to Markdown format."""
    markdown_lines = []
    tag_name = html_list.name
    for index, li in enumerate(html_list.find_all("li"), start=1):
        prefix = "* " if tag_name == "ul" else f"{index}. "
        markdown_lines.append(f"{prefix}{li.text.strip()}")
    return "\n".join(markdown_lines)


def replace_lists_with_markdown(body):
    """Replace all lists in the body with their Markdown representation."""
    for html_list in body.find_all(['ul', 'ol']):
        markdown = html_list_to_markdown(html_list)
        placeholder = NavigableString(markdown)
        html_list.replace_with(placeholder)


def html_to_markdown(file_path):
    # Open and read the HTML file
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()

    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extract the body content, if the body tag exists
    body = (soup.body if soup.body else soup)

    # Convert headings
    for h_tag in body.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
        level = int(h_tag.name[1])
        h_tag.replace_with('#' * level + ' ' + h_tag.text + '\n')

    # Dedent the paragraphs
    for p_tag in body.find_all('p'):
        p_tag.string = dedent(p_tag.text)

    # Remove <p> tags but keep their content
    for p_tag in body.find_all('p'):
        p_tag.unwrap()

    # Remove scripts
    for script_tag in body.find_all('script'):
        script_tag.decompose()

    # Convert links to Markdown format
    for a_tag in body.find_all('a'):
        href = a_tag.get('href', '')
        text = a_tag.text
        markdown_link = f"[{text}]({href})"
        a_tag.replace_with(markdown_link)

    # Remove <br> tags
    for br_tag in body.find_all('br'):
        br_tag.replace_with('\n')

    # Remove <br> tags
    for br_tag in body.find_all('br'):
        br_tag.replace_with('\n')

    # Convert <pre> tags to Markdown code blocks
    for pre_tag in body.find_all('pre'):
        code_content = pre_tag.text
        pre_tag.replace_with('```\n' + code_content + '\n```')

    # Since <div> and <img> tags are to be kept as is, we don't process them here.

    # Get rid of divs that have no content
    for div in body.find_all('div'):
        if not div.text.strip():
            div.decompose()

    # Get rid of id='wrap' divs
    for div in body.find_all('div', id='wrap'):
        div.unwrap()
    for div in body.find_all('div', id='main'):
        div.unwrap()

    # Ged rid of divs that have only another div as content
    for div in body.find_all('div'):
        if len(div.find_all('div')) == 1 and not div.text.strip():
            div.unwrap()

    # change all of the images that are relative the url doesn't start
    # with http, to be relative to the current directory
    for img in body.find_all('img'):
        src = img.get('src')
        if not src.startswith('http'):
            img['src'] = './images/' + src.split('/')[-1]

    replace_lists_with_markdown(body)

    # Extract the body content as html
    md = str(body.prettify())
    md = html.unescape(md)
    md = md.strip() + "\n"

    # Strip off the opening <body> and closing </body>
    md = md.replace("<body>", "").replace("</body>", "")

    md = re.sub(r'\xa0', ' ', md)
    md = re.sub(r'</?div.*>', '', md)

    # Remove multiple blank lines
    md = re.sub(r'\n{3,}', '\n\n', md)

    # Remove any leading spaces before MD Headins
    md = re.sub(r'\n\s*#', '\n#', md)

    # Remove any leading spaces before tripp-backtic code blocks.
    md = re.sub(r'\n\s*```', '\n```', md)

    # Remove leading spaces for before  text, but not inside triple backticks
    o = ''
    do_strip = True

    for line in md.splitlines():
        if line.startswith('```'):
            do_strip = not do_strip
        if do_strip:
            line = line.strip()

        # Re add spaces around headings.
        if line.startswith('#'):
            line = '\n' + line + '\n'

        o += line + '\n'

    return o


def _proc_html(f):
    """Download the assets of a recipe and convert it to markdown."""

    from .walk import get_lmla
    from .util import extract_urls, download_webpage_assets

    print("Downloading ", f)
    web_dir = f.parent / '.web'
    web_dir.mkdir(exist_ok=True)

    urls = extract_urls(f.read_text())

    try:
        if not urls or len(urls) < 1:
            # Thre is no link in the recipe text, so it
            # is the text itself.
            download_webpage_assets(f.read_text(), web_dir)
        else:
            download_webpage_assets(urls[0], web_dir)

    except Exception as e:
        print("ERROR: Failed to download ", f)
        print(e)

    # f.rename(web_dir / f.name)




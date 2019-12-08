#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader
from markdown import markdown
from pathlib import Path

import logging

# not using this yet
def content():
    return {'helloworld': 'foobar'.upper()}


# this assumes that your project is here for now this is fine Im exhausted.
def from_jinja2(filename, 
                templates_dir=str(Path().home().joinpath('Projects', 'simpai', 'example', 
                                                         'templates').resolve())
                ):
    logging.debug(f"templates_dir: {templates_dir}")
    
    file_loader = FileSystemLoader(templates_dir)
    env = Environment(loader=file_loader)
    
    layout = env.get_template(filename)
    return layout.render(content=content())

def from_markdown(md):
    logging.debug(f'{md} is {type(md)}')
    try:
        return markdown(md.read_text())
    except TypeError:
        logging.error(f'TypeError on render_markdown')
        if type(md) == str:
            return markdown(md)
    return

logging.info(f'loaded simpai.render')


if __name__ == '__main__':
    pass

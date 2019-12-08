import example.pagerender as render
import example.pageconfig as c

from simpai.sites import Site
from simpai.data import jdump, jload

from pprint import pprint
from pathlib import Path

import logging, os

# for whatever reason my log files are not working...
logging.basicConfig(filename='vfghio_gen.log', filemode='w', level=logging.DEBUG)
logging.debug("sdfasadfsd")

if __name__ == '__main__':
    
    site = Site("virufac.github.io", 'virufac.github.io')
    logging.info(f"initalized site {site}")
    
    site.add_menu_entry('Index', 'index.html',
                        "Site root. This is where you currently are. \
                            It's good to be mindful of things like that, apparently.")
    site.add_menu_entry('Writing', 'writing/writing.html',
                        "Posts, essays, manifestoes, rants, stories, and graphomanic nonsense \
                            of a Dadaist quality. Words that I end up posting.")
    site.add_menu_entry('Projects', 'projects/projects.html',
                        "a portfolio and devblog of work that may already be abandonware! \
                            Feel free to fork or pull request.")
    site.add_menu_entry('Education', 'education/education.html',
                        "Documentation on my self-taught curriculum of programming, infosec, \
                            open source, and technology; resources for newbies.")
    site.add_menu_entry('Self', 'self/self.html',
                        "Taking self as its only parameter, this Directory instance has \
                            few attributes: those being, links to my social media.")
    logging.info(f"initalized site 5 menu entries...")
    
    
    site.add_byline('The "Professional" Website of Shænᚱ, AKA viruFac(), AKA... ')
    logging.info(f"initalized site byline")
    
    
    
    site.add_footer_line('All words written on these pages are my words. All rights reserved. ', quip=True)
    site.add_footer_line('I am not using cookies or attempting to log your usage of this website at all.')
    site.add_footer_line('GitHub probably is though.', quip=True)
    logging.info(f"initalized three ptags of a footer...")
    
    
    site.add_welcome('Hello and thank you for briefly departing from proprietary Web 2.0 to peruse my directory of pages. My name is Shæn,' + 
                     ' and I am responsible for them as much as any person is singularly responsible for anything that has ever been developed, open source and otherwise.')
    site.add_welcome('This directory will speak for itself.', quip=True)
    logging.info(f"initalized two ptags of a welcome...")
    
    
    site.add_author('viruFac', 'viruFac@protonmail.com', '/self/self.html')
    logging.info(f"added author...")
    
   
    site_json = Path().cwd().joinpath('test.json').resolve()
    logging.debug(f"site_json: {site_json}")
    
    jdata = site.add_attrs_to_dict()
    logging.debug(f"jdata: {jdata}")
    
    pprint(jdata)
    
    #trying to fix this:
    try:
        jdump(jdata, site_json)
    except:
        print("jdump didn't work")

    
    html = render.from_jinja2('index.html')
    logging.debug(f"html: {html}, rendered from templates...")
    
    with open('./example/output/index.html', 'w') as fo:
        fo.write(html)
    
        

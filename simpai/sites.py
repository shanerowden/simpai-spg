from pathlib import Path
from pprint import pprint
from simpai import config as c


class Site:
    def __init__(self, name, url, local=Path.cwd().resolve(), welcome=c.welcome):
        self.name = name
        self.local = local
        self.url = url
        self.menu = {}
        self.menu_links = 0
        self.welcome = welcome
        self.bylines = {'index': [],
                        'other': []}
        self.footer = {'main': [],
                       'other': []}
        self.author = {}
        
    def add_menu_entry(self, name, link, descrip=None, posts=False):
        self.menu_links += 1
        self.menu[self.menu_links] = {'name': name,
                              'link': c.http + self.url + '/' + link,
                              'descrip': descrip}
        if posts:
            print("This is where posts dir should go.")
        
    def add_byline(self, line, page='index'):
        ls = [l for l in self.bylines[page]]
        ls.append(line)
        self.bylines[page] = ls
        
    def add_footer_line(self, line, name='main', quip=False):
        if quip:
            ptag = '<p class="quips">'
        else:
            ptag = '<p>'
        line = ptag + line + '</p>'
        ls = [l for l in self.footer[name]]
        ls.append(line)
        self.footer[name] = ls

    def add_welcome(self, line, quip=False):
        if quip:
            ptag = '<p class="quips">'
        else:
            ptag = '<p>'
        line = ptag + line + '</p>'
        self.welcome = [l for l in self.welcome] + [line]
        
    def add_author(self, name, email, page):
        page = self.url + page
        self.authors = {name: (email, page)}
        
    def add_attrs_to_dict(self):
        d = {}
        d['name'] = self.name
        d['local'] = self.local
        d['url'] = self.url
        d['menu'] = self.menu
        d['menu_links'] = self.menu_links
        d['welcome'] = self.welcome
        d['footer'] = self.footer
        d['bylines'] = self.bylines
        d['authors'] = self.author
        return d

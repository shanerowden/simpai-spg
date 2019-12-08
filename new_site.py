#!/usr/bin/env python3

from simpai import config as c
from jinja2 import Environment, FileSystemLoader
from markdown import markdown
from pathlib import Path
import os, sys, shutil, logging

SCRIPT, *site_name = sys.argv

logging.basicConfig(filename=Path().cwd().joinpath('new_site.log'), filemode='w', level=logging.DEBUG)
    

# This needs to be cleaned up...
def new_site_start(name=site_name[0], root=Path().cwd(), theme='virulence.factor'):
    path_root = root.resolve()
    logging.debug(f'path_root: {path_root}')
    
    path_theme = path_root.joinpath('themes', theme)
    logging.debug(f'path_theme: {path_theme}')
    
    path_gen = path_root.joinpath(str(name))
    logging.debug(f'path_gen: {path_gen}')


    path_gen_temps = path_gen.joinpath('templates')
    logging.debug(f'path_gen_temps: {path_gen_temps}')

    site_paths = {'path_root': path_root, 'path_theme': path_theme,
                  'path_gen': path_gen, 'path_gen_temps': path_gen_temps}
    
    
    if path_gen.exists() and path_gen.is_dir():
        print(f"Site already exists named {path_gen.name}")
    else:
        path_gen.mkdir()
        logging.info(f'made dir {path_gen}')
        
        for directory in c.FILE_TREE['site_gen'].keys():
            p = path_gen.joinpath(directory)
            p.mkdir()
            logging.info(f'made dir {p}')
            
    if path_theme.exists():
        temps_tree = {'path_layout': path_theme.joinpath('html', 'layout'),
                      'path_includes': path_theme.joinpath('html', 'layout', 'includes'),
                      'path_extends': path_theme.joinpath('html', 'layout', 'extends')}
        
        for path in temps_tree.values():
            strpath = str(path)
            if not path.exists() or not path_gen_temps.exists():
                print(f"{strpath} or {str(path_gen_temps)} does not exist")
                return
            else:
                files = [f for f in os.listdir(strpath) if not os.path.isdir(f)]
                for f in files:
                    f = path.joinpath(f).resolve()
                    if not f.is_dir():
                        src = str(f)
                        dst = str(path_gen_temps.joinpath(f.name))
                        shutil.copy2(src, dst)
                        logging.info(f'copied {src} to {dst}')
                        
    stylesheets = path_theme.joinpath('style').resolve()
    for css in os.listdir(str(stylesheets)):
        if css.endswith('.css'):
            src = str(stylesheets.joinpath(css).resolve())
            dst = str(path_gen.joinpath('css', css).resolve())
            shutil.copy2(src, dst)
            logging.info(f'copied {src} to {dst}')
        elif css.endswith('.scss'):
            compile_scss(css)
            
    copy_python_files(['config.py', 'render.py', '__init__.py'], site_paths)
    logging.warning('REMEMBER TO IMPORT THESE FILES FROM YOUR PROJECT NOT FROM SIMPAI')
        
    return site_paths








def compile_scss(scss):
    print("Not finished yet.")
    logging.info(f'not finished scss compiling yet')
    return scss


def copy_python_files(files_to_copy, path_objs):
    path_root = path_objs['path_root']
    path_gen = path_objs['path_gen']
    for f in files_to_copy:
        src = path_root.joinpath('simpai', f).resolve()
        
        if f == '__init__.py':
            dst = path_gen.joinpath(f).resolve()
        else:
            dst = path_gen.joinpath('page' + f).resolve()
            
        shutil.copy2(str(src), str(dst))
        logging.info(f'copied {src} to {dst}')
    



if __name__ == '__main__':
    new_site_start()

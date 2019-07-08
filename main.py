#!/usr/bin/env python3

# viruFac, @shaen@hackers.town
# http://virufac.github.io
# virufac@protonmail.com
# APGL 3.0

from datetime import datetime
import pageconfig as cfg
import subprocess
import sys
import os

def get_title(title=cfg.TITLE):
    return title

def get_element_list(path="template.html"):
    with open("template.html", 'r') as fo:
        template = fo.readlines()
        return [(idx, elem) for idx, elem in enumerate(template)]

def replace_element(insert, placeholder):
    for line in template_html:
        if line[1] == placeholder:
            template_html[line[0]] = (line[0], insert)

def get_css_element(filename=cfg.CSS_FILE):
    head = '<link href="/css/'
    tail = '" rel="stylesheet" type="text/css" media="all">'
    return "{}{}{}".format(head, filename, tail)

def build_page(template_list, page_name):
    if not page_name + ".html" in os.listdir():
        with open(page_name + ".html", 'w') as fo:
            for line in template_list:
                fo.write(line[1])
    else:
        print("Page exists. Cannot write file.")
        page_name = input("Enter new page name: ")
        build_page(template_list, page_name)

def initialize_post():
    confirm = input("Write a new post? Y/n? ").lower()
    if confirm.startswith("y"):
        making_new_post = True
        if os.path.isdir(cfg.POST_PATH):
            os.chdir(cfg.POST_PATH)
            global subtitle
            subtitle = input("What is the title of this post?\n> ")
            posted_on = datetime.now().strftime('Posted on %B %d, %Y at %H:%M Hours')
            timestamp = datetime.now().strftime('%B%d%Y-%H%M')
            if not os.path.exists(f"{cfg.POST_PATH}{timestamp}.txt"):
                with open(cfg.POST_PATH + timestamp + ".txt", 'w') as fo:
                    fo.write("## " + subtitle + " ##\n")
                    fo.write("###" + posted_on + "###\n")
                    fo.write("#" * (len(posted_on) + 6))
                    fo.write("\n")
                    return cfg.POST_PATH + timestamp + ".txt", subtitle, posted_on, timestamp
            else:
                print("File Exists. Cannot Write New Post.")
                sys.exit(1)
        else:
            print("Check postconfig.py for a absolute path to dir, POST_PATH")
            sys.exit(1)
    else:
        making_new_post = False
        if not making_new_post:
            print("Then wtf are you doing, bruv?")
            # TODO Why does "No" option error?...


cwd = os.getcwd()
template_html = get_element_list()
title = get_title()
stylesheet = get_css_element()
subtitle = ""
path, subtitle, posted_on, timestamp = initialize_post()
os.chdir(cwd)

element_changes = [(title, cfg.TITLEBAR), (stylesheet, cfg.STYLESHEET), (subtitle, cfg.SUBTITLE),
                   (title, cfg.TITLEHEAD), (cfg.CURRENT_VERSION, cfg.VERSION),
                   (cfg.DEFAULT_BYLINE, cfg.BYLINE), (cfg.TEMPLATE_RELEASENOTE, cfg.RELEASENOTE),
                   (cfg.TEMPLATE_ENTRIES, cfg.ENTRIES), (cfg.TEMPLATE_FIRSTBLOCK, cfg.FIRSTBLOCK),
                   (cfg.TEMPLATE_PAGINATION, cfg.PAGINATION)]

for elem, placeholder in element_changes:
    replace_element(elem, placeholder)

writing_post = True
while writing_post:
    print("Edit file at: " + path)
    inp = input("Please write your post to the file above... Save, then type 'MAKE' and press RETURN ... ")
    if inp == "MAKE":
        writing_post = False
        break

with open(path) as fo:
    post_data = fo.readlines()
    post_data = [line for line in post_data if not '##' in line]
    post_data = "".join(post_data)

replace_element(post_data, cfg.POST)
build_page(template_html, cfg.POSTED_PATH + timestamp)
print("Page Generated here:")
print(cfg.POSTED_PATH + timestamp)


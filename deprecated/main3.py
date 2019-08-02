#!/usr/bin/env python3

# viruFac, @shaen@hackers.town
# http://virufac.github.io
# virufac@protonmail.com
# APGL 3.0

from datetime import datetime
import pageconfig as cfg
import sys
import os

# Allows you to retitle website, default gets title from pageconfig.txt
#def get_title(title=cfg.TITLE):
    #return title

# Takes template and saves all of its lines to list with indexed tuple
##def get_element_list(path="template.html"):
    #with open(path) as fo:
        #template = fo.readlines()
        #return [(idx, elem) for idx, elem in enumerate(template)]

#def replace_element(insert, placeholder, template):
    #for line in template:
        # if content of line equals placeholder
        #if line[1] == placeholder:
            # the index of the line is used to replace the line in the list
            #template[line[0]] = (line[0], insert)

#def get_css_element(filename=cfg.CSS_FILE):
    #head = '<link href="/css/'
    #tail = '" rel="stylesheet" type="text/css" media="all">'
    #return "{}{}{}".format(head, filename, tail)

# writes html file
#def build_page(template_list, page_name):
    #if second_phase or not page_name + ".html" in os.listdir():
        #with open(page_name + ".html", 'w') as fo:
            #for line in template_list:
                #fo.write(line[1])
    ## if filename already exists, chance to rename file
    #else:
        #print("Page exists. Cannot write file.")
        #page_name = input("Enter new page name: ")
        #build_page(template_list, page_name)

# creates txt file for writing post
#def initialize_post():
    #confirm = input("Write a new post? Y/n? ").lower()
    #if confirm.startswith("y"):
        making_new_post = True
        #if os.path.isdir(cfg.POST_PATH):
            #os.chdir(cfg.POST_PATH)
            #subtitle = input("What is the title of this post?\n> ")
            #posted_on = datetime.now().strftime('Posted on %B %d, %Y at %H:%M Hours')
            #timestamp = datetime.now().strftime('%B%d%Y-%H%M')
            #if not os.path.exists(f"{cfg.POST_PATH}{timestamp}.txt"):
                #with open(cfg.POST_PATH + timestamp + ".txt", 'w') as fo:
                    #fo.write("## " + subtitle + "\n")
                    #fo.write("###" + posted_on + "\n")
                    #len(subtitle) + 3, len(posted_on) + 3))
                    #fo.write("\n")
                    #return cfg.POST_PATH + timestamp + ".txt", subtitle, posted_on, timestamp
            # if file already exists
            #else:
                #print("File Exists. Cannot Write New Post.")
                #sys.exit(1)
        # if path doesn't exist
        else:
            #print("Check postconfig.py for a absolute path to dir, POST_PATH")
            #sys.exit(1)
    # if not yes on confirm
    else:
        current_file = input("Enter file path for html to edit... ")
        os.path.abspath(current_file)
        template_html = get_element_list(current_file)
        action = input("Paginate? Y/n ").lower()
        if action.startswith('y'):
            paginate(template_html)



        #sys.exit(1)

# Optional function calls
def paginate(current_file):
    template_html = get_element_list(current_file + ".html")
    os.chdir(cfg.POSTED_PATH)
    files = os.listdir()
    files.sort()

    if len(files) == 1: # First Post
        pagination_changes = [(cfg.TEMPLATE_PAGIN_NEXT, cfg.PAGIN_NEXT)]
    elif len(files) > 1: # Two or More Posts

        pagination_changes = [(cfg.TEMPLATE_PAGIN_PREV, cfg.PAGIN_PREV),
                              (cfg.TEMPLATE_PAGIN_NEXT, cfg.PAGIN_NEXT)]
        prev_link = "/posts/" + files[-2]
        next_link = "/index.html"
    for elem, placeholder in pagination_changes:
        replace_element(elem, placeholder, template_html)
    build_page(template_html, current_file)

    template_html = get_element_list(current_file + ".html")
    pagination_changes = [(prev_link, "<!-- ,$PREV_LINK(), -->"),
                          (next_link, "<!-- ,$NEXT_LINK(), -->")]
    for elem, placeholder in pagination_changes:
        replace_element(elem, placeholder, template_html)
    build_page(template_html, current_file)
    os.chdir(cwd)


def make_archive(template_list):
    print("Feature I Haven't Finished Yet is a Feature")

def add_description(template_list):
    print("Feature I Haven't Finished Yet is a Feature")

def add_footnote(template_list):
    print("Feature I Haven't Finished Yet is a Feature")


# get basic information and write txt file
#cwd = os.getcwd()
second_phase = False
#template_html = get_element_list()
#title = get_title()
#stylesheet = get_css_element()
#path, subtitle, posted_on, timestamp = initialize_post()
#os.chdir(cwd)

# confirm to build html page screen
#writing_post = True
#while writing_post:
    #print("Edit file at: " + path)
    #inp = input("Please write your post to the file above... Save, then type 'MAKE' and press RETURN ... ")
    #if inp == "MAKE":
        #writing_post = False
        #break

## read txt after post is written
#with open(path) as fo:
    #post_data = fo.readlines()
    #post_data = [line for line in post_data if not '##' in line]
    #post_data = "".join(post_data)


# changes as tuple: (to-be-inserted, specified-placeholder) to appear in new posts
#element_changes = [(title, cfg.TITLEBAR),
                   #(stylesheet, cfg.STYLESHEET),
                   #(subtitle, cfg.SUBTITLE),
                   #(title, cfg.TITLEHEAD),
                   #(cfg.CURRENT_VERSION, cfg.VERSION),
                   #(cfg.DEFAULT_BYLINE, cfg.BYLINE),
                   #(post_data, cfg.POST)]

#optional_changes = {'TEMPLATE_RELEASENOTE': (cfg.TEMPLATE_RELEASENOTE, cfg.RELEASENOTE),
                    #'TEMPLATE_ENTRIES': (cfg.TEMPLATE_ENTRIES, cfg.ENTRIES),
                    #'TEMPLATE_FIRSTBLOCK': (cfg.TEMPLATE_FIRSTBLOCK, cfg.FIRSTBLOCK),
                    #'TEMPLATE_PAGINATION': (cfg.TEMPLATE_PAGINATION, cfg.PAGINATION)}

## Run optional dialogue; when finished optional_changes will only have selected options
#for option in list(optional_changes):
    #inp = input(f"Add OPTIONAL element for {option}? Y/n\n> ").lower()
    #if inp.startswith('y'):
        #print(f"\tAdded {option}")
        #element_changes.append(optional_changes[option])
    #else:
        #print(f"\tSkipped {option}")
        #del optional_changes[option]

# make the basic element changes
for elem, placeholder in element_changes:
    replace_element(elem, placeholder, template_html)
build_page(template_html, cfg.POSTED_PATH + timestamp)

# display html file and establish current_file
current_file = cfg.POSTED_PATH + timestamp
print("Page Generated here: " + current_file + ".html")
second_phase = True

# Optional Changes checked from the var and executed in function
if 'TEMPLATE_PAGINATION' in list(optional_changes):
    paginate(current_file)
if 'TEMPLATE_ENTRIES' in list(optional_changes):
    make_archive(current_file)
if 'TEMPLATE_FIRSTBLOCK' in list(optional_changes):
    add_description(current_file)
if 'TEMPLATE_RELEASENOTE' in list(optional_changes):
    add_footnote(current_file)

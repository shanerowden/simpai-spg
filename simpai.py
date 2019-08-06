#!/usr/bin/env python3

import os, sys, subprocess, random, json
from datetime import datetime
from string import Template
import pageconfig as pc


class Page:
    # Initializes Attributes That All Pages Have
    def __init__(self, title, byline, version, css_path, html_path, date):
        self.post = dict()
        self.post['title'] = title
        self.post['byline'] = byline
        self.post['version'] = version
        self.post['css_path'] = css_path
        self.post['css_elem'] = '<link href="/css/' + self.post['css_path'] \
                                + '"rel="stylesheet" type="text/css" media="all">'        
        self.post['html_path'] = html_path
        self.post['html_link'] = os.path.join(pc.SITE_URL, \
                                '/'.join(self.post['html_path'].split(os.sep)[-2:]))

        self.post['date'] = date
        self.post['id_no'] = 'undefined'

        
    def open_html(self):
        subprocess.run([pc.BROWSER, self.post['html_path']])


    # Assembles Dictionary of Changes For REPLACE_ELEMENT function
    def get_elementary_changes(self):
        changes = {'TITLEBAR': self.post['title'],
                   'CSS': get_css_element(get_css_file()),
                   'TITLEHEAD': self.post['title'],
                   'VERSION': self.post['version'],
                   'BYLINE': self.post['byline'],
                   'SUBTITLE': self.subtitle,
                   'POST': self.post_data}
        return changes

    # Inserts Optional Page Blocks
    def make_optional_changes(self, changes, template):
        global paginate_last_page_switch
        paginate_last_page_switch = False
        self.post['option_img'] = False
        self.post['option_archive'] = False
        self.post['option_releasenote'] = False
        self.post['option_pagin'] = False

        for optional in changes:
            if optional == 'IMG':
                self.post['option_img'] = True
                while True:
                    self.img_path = input("\nEnter Path to Image\n> ")
                    if os.path.exists(pc.SITE_PATH + pc.IMG_PATH + self.img_path):
                        break
                self.img_path = pc.SITE_URL + pc.IMG_PATH + self.img_path
                self.post['img_path'] = self.img_path
                template = replace_element(template, {'IMG_PATH':self.img_path})

            if optional == 'ARCHIVE':
                l, d = get_posts(pc.POSTS_JSON)
                if len(l) >= 2:
                    self.post['option_archive'] = True
                    # Truncate archive.html
                    with open(pc.ARCHIVE_PATH, 'w') as fo:
                        fo.write('')
                    # Instantiate New Archive Insert
                    arc = Archive(*get_page_params())
                    # Insert Archive into Page as Block
                    with open(pc.ARCHIVE_PATH) as fo:
                        insert = fo.read()
                        template = replace_element(template, {'ARCHIVE_PAGE':insert})

            if optional == 'RELEASENOTE':
                self.post['option_releasenote'] = True
                self.releasenote = input("\nType a Release Note\n> ")
                self.post['releasenote'] = self.releasenote
                template = replace_element(template, {'VERSION': pc.CURRENT_VERSION,
                                                      'TIMESTAMP': get_date()[2],
                                                      'RELEASEUPDATE': self.releasenote})

            if optional == 'PAGINATION':
                self.post['option_pagin'] = True
                l, d = get_posts(pc.POSTS_JSON)
                # Get Previous Link From Last Page
                if len(l) >= 2: 
                    self.post['prev_link'] = d[l[-2]]['html_link']
                    template = replace_element(template, {'PREV_LINK': self.post['prev_link'],
                                                          'PREV_NAME': 'PREVIOUS'})
                else: # Remove placeholders if first page
                    template = replace_element(template, {'PREV_LINK': '',
                                                          'PREV_NAME': ''})
                # Open Last Page and Insert Link to Current Page
                if len(l) >= 2:
                    paginate_last_page_switch = True
                
        return template

    # Get Count of Files in Directory
    def count_posts(self, posts_dir=pc.POSTS_JSON):
        pl, _ = get_posts(posts_dir)
        return len(pl)

    # Write HTML to File
    def build_page(self, template):
        if os.path.isdir(pc.HTML_PATH):
            cwd = os.getcwd()
            os.chdir(pc.HTML_PATH)
            # Second Phase is a Rebuild for Pagnation
            if not self.post['html_path'] in os.listdir():
                with open(self.post['html_path'], 'w') as fo:
                    fo.write(template)
            else:
                print("Page Exists. Cannot write file.")
            os.chdir(cwd)
        else:
            print("Give Absolute Path in pageconfig.py for HTML_PATH and Make Sure is Directory")
            sys.exit(1)
        return


class Archive(Page):
    # Initialize Archive Tempate Insert
    def __init__(self, title, byline, version, css_path, html_path, date):
        super().__init__(title, byline, version, css_path, html_path, date)
        self.post_count = self.count_posts()
        # Get Post Objects in Dict and List Them
        l, d = get_posts()
        l.pop() # Remove Most Recent Post From List
        l.reverse() # So Posts Will Be Listed By Most Recent
        for i in l: # For Each Post, Make an Archive Entry
            arc_html = make_html_template(pc.TEMPLATE_ENTRY)
            arc_html = replace_element(arc_html, \
                dict([("ENTRYLINK", d[str(i)]['html_link']),
                      ("ENTRYNAME", '-'.join(d[str(i)]['subtitle'].split(' ')).lower()),
                      ("ENTRYDESC", d[str(i)]['post_head']),
                      ("DATE", d[str(i)]['date'][2])]))
            # Uses TMP File to Replace Elements with Same Placeholders for Each Post
            with open('archive.tmp', 'w') as temp_file:
                temp_file.write(arc_html.template)
            jdata = load_json()
            self.post['archive_entry'] = arc_html.template
            dump_json(self.post, jdata)
            #Add the TMP File to a Blank Archive Template in Append Mode
            with open(pc.ARCHIVE_PATH, 'a') as fo:
                fo.write(arc_html.template+"\n")


class Post(Page):
    # Initialize a Regular Post in a TXT File
    def __init__(self, title, byline, version, css_path, html_path, date):
        super().__init__(title, byline, version, css_path, html_path, date)
        self.post['id_no'] = self.get_id_no()
        self.post['id_no'] = self.post['id_no']
        cwd = os.getcwd()
        confirm = input("Write a new post? Y/n? ").lower()
        if confirm.startswith('y'):
            # Check the Paths Are Valid
            if os.path.isdir(pc.TXT_PATH):
                os.chdir(pc.TXT_PATH)
                self.subtitle = input("What is the title of this post?\n")
                # If the TXT File Doesn't Already Exist, Name It by Date
                if not os.path.exists(f"{pc.TXT_PATH}{self.post['date'][0]}.txt"):
                    self.txt_path = f"{pc.TXT_PATH}{self.post['date'][0]}.txt"
                    with open(self.txt_path, 'w') as txt:
                        # Write the title and date of the post
                        txt.write(self.subtitle + "\n")
                        txt.write(self.post['date'][1] + "\n")
                        # Draw a Separating Line Equal to the Length of Heading
                        txt.write("#" * max(len(self.subtitle), len(self.post['date'][1])+2))
                        txt.write("\n")
                        os.chdir(cwd)
                        return
                else:
                    print("File exists. Cannot write new post.")
                    sys.exit(1)
            else:
                print("Check pageconfig.py for an absolute path to dir, TXT_PATH")
                sys.exit(1)
        else:
            sys.exit(1)

    # Executes TXT File for Post in Editor of Choice
    def open_txt(self):
        subprocess.run([pc.EDITOR, self.txt_path])
        # Read the TXT After Post is Written
        with open(self.txt_path) as fo:
            self.post_data = fo.readlines()
            # If the the Subtitle is Changed, Edit the Shelf
            self.subtitle = self.post_data[0][:-1]
            self.post['subtitle'] = self.subtitle
            # Pretty Sure This Line isn't Necessary, But Will Check Later
            self.post_data = [line for line in self.post_data]
            self.post_data.pop(0) # These Pops Are
            self.post_data.pop(0) # For Removing
            self.post_data.pop(0) # The Heading
            # Then all the lines are joined into one String
            self.post_data = "".join(self.post_data)
            self.post['post_data'] = self.post_data
            # The first 100 characters of the post are saved for archive preview
            self.post_head = self.post_data.split('\n')[0][:100]
            self.post['post_head'] = self.post_head

    # The ID_NO is Used to Store and Pull Post Objects
    def get_id_no(self, path=pc.TXT_PATH):
        # If ID Hasn't Been Saved...
        if self.post['id_no'] == 'undefined':
            # ...Use the Number of TXT Files to Call It
            jdata = load_json()
            file_count = len(jdata.keys())
            return str(file_count)
        else: # Otherwise Return the ID
            return str(list(jdata.keys())[-1])

# Opens and HTML File and Returns One String
def get_html_file(html_file=pc.TEMPLATE_FILE):
    with open(html_file) as fo:
        data = fo.read()
    return data

# Transforms HTML String into Template Object for Inserts
def make_html_template(data):
    t = Template(data)
    return t

# Build CSS element
def get_css_element(css_file):
    head = '<link href="/css/'
    tail = '" rel="stylesheet" type="text/css" media="all">'
    return head + css_file + tail

# Takes Template Object and Dictionary of Changes
def replace_element(html, changes):
    # Hack to Prevent an Empty Dict From Crashing Script
    if list(changes.keys()) == []:
        return html
    # Make Each Change Individually, and Repeat
    for change in changes.keys():
        new_html = html.safe_substitute(changes)
        # Reform the Template to Reflect Change Just Made
        new_template = make_html_template(new_html)
    # After All Changes Are Made, Return
    return new_template

# This is Where You Can Add Optional Inserts
# Make Sure to Update p.make_optional_changes() if you add any here.
def select_options():
    # Every Possible Change, {PLACEHOLDER: INSERT}
    changes = {'IMG': pc.TEMPLATE_IMG,
           'ARCHIVE': pc.TEMPLATE_ARCHIVE,
           'RELEASENOTE': pc.TEMPLATE_RELEASENOTE,
           'PAGINATION': pc.TEMPLATE_PAGINATION}
    removal_list = [] # Initialize a List for Removed Items
    for option in changes.keys():
            inp = input(f"Add OPTIONAL element for {option}? Y/n > ").lower()
            if inp.startswith('y'):
                print(f"\tAdding {option}\n")
            else:
                print(f"\tSkipped {option}\n")
                removal_list.append(option)
    # Remove Options from Changes Dict After Iteration
    for option in removal_list:
        del changes[option]
    return changes, removal_list

# Placeholders for Optional Elements Must Be Removed From Final HTML
def remove_placeholders(html, removed):
    changes = {k: '' for k in removed}
    new_template = replace_element(html, changes)
    return new_template

#Open the JSON a List and Dict
def get_posts(path=pc.POSTS_JSON):
    jdata = load_json(path)
    return list(jdata.keys()), jdata

def load_json(path=pc.POSTS_JSON):
    while True:
        if os.path.exists(path):
            with open(path, 'r') as fo:
                json_data = json.load(fo)
                break
        else:
            posts = {'0' : None}
            with open(path, 'w') as fo:
                json.dump(posts, fo)
    return json_data

def dump_json(post_dict, json_data, path=pc.POSTS_JSON):
    json_data[post_dict['id_no']] = post_dict
    
    if '0' in list(json_data.keys()):
        del json_data['0']
        
    with open(path, 'w') as fo:
        json.dump(json_data, fo, indent=2)
    
def paginate_last_page(po):
    jdata = load_json()

    for key in list(jdata.keys()):
        try:
            if jdata[key]['option_pagin'] == True:
                next_link = jdata[str(int(key)+1)]['html_link']
                print(next_link)
                jdata[key]['next_link'] = next_link
        except KeyError:
            current_page = key
            print(f'Current Page: {key}')
            last_page_id = str(int(key) - 1)
            print(f'Last Page: {last_page_id}')
            
    with open(pc.POSTS_JSON, 'w') as fo:
        json.dump(jdata, fo, indent=2)

    # Opening Last Page
    with open(jdata[last_page_id]['html_path']) as fo:
        template_lines = fo.readlines()
        
    # Index Lines for Comment Removal of Next Page Nav Link
    template_lines = [(idx, elem) for idx, elem in enumerate(template_lines)]
    # Search and Replace by Index
    for line in template_lines:
        if line[1].startswith('<!--<a class="next"'):
            template_lines[line[0]] = (line[0], \
                '<a class="next" href="$NEXT_LINK">$NEXT_NAME</a></nav>')
            print("shit replaced")
            
    # Write the lines to temporary file, without indexes
    template_lines = [line[1] for line in template_lines]
    with open("lastpage.html", 'w') as fo:
        for line in template_lines:
            fo.write(line+'\n')
            
    # Send temp file back through process.
    data = get_html_file("lastpage.html")
    html = make_html_template(data)
    html = replace_element(html, {'NEXT_LINK': jdata[current_page]['html_link'],
                                  'NEXT_NAME': 'NEXT'})

    rebuild_page(jdata[last_page_id]['html_path'], html.template)
    paginate_last_page_switch = False
    return

def rebuild_page(page, template):
    cwd = os.getcwd()
    os.chdir(pc.HTML_PATH)
    with open(page, 'w') as fo:
        fo.write(template)
    os.chdir(cwd)
    return
    
# Get Basic Page Parameters Mostly from the PAGECONFIG File
def get_title(title=pc.TITLE):
    return title
def get_byline(byline=pc.DEFAULT_BYLINE):
    return byline
def get_version(version=pc.CURRENT_VERSION):
    return version
def get_css_file(css=pc.CSS_FILE):
    if css == 'random':
        die_roll = random.randint(1, 360)
        css = "color{}.css".format(die_roll)
    return css
def get_html_path(path=pc.HTML_PATH):
    date = get_date()
    return path + date[0] + ".html"
def get_date():
    posted_on = datetime.now().strftime('Posted on %B %d, %Y at %H:%M Hours')
    timestamp = datetime.now().strftime('%B%d%Y-%H%M').lower()
    short = datetime.now().strftime('%m/%d/%y')
    return timestamp, posted_on, short

# Design a Tuple for Unpacking Params into a Page Instantiation
def get_page_params():
    title = get_title()
    byline = get_byline()
    version = get_version()
    css_file = get_css_file()
    html_path = get_html_path()
    date = get_date()
    return (title, byline, version, css_file, html_path, date)

# Complete Process for Building a New Post
def write_post():
    jdata = load_json()
    p = Post(*get_page_params())
    p.open_txt()
    changes = p.get_elementary_changes()
    data = get_html_file()
    html = make_html_template(data)
    html = replace_element(html, changes)
    changes2, removed = select_options()
    html = replace_element(html, changes2)
    html = remove_placeholders(html, removed)
    html = p.make_optional_changes(list(changes2.keys()), html)
    p.build_page(html.template)
    dump_json(p.post, jdata)
    jdata = load_json()
    if paginate_last_page_switch:
        paginate_last_page(p)
    jdata = load_json()
    dump_json(p.post, jdata)
    return html, changes, changes2, removed, p

if __name__ == '__main__':
    html, changes, changes2, removed, p = write_post()
    

import os, sys, subprocess, shelve
from datetime import datetime
from string import Template
import pageconfig as pc

class Page:
    # Initializes Attributes That All Pages Have
    def __init__(self, title, byline, version, css_path, html_path, date):
        self.title = title
        self.byline = byline
        self.version = version
        self.css_path = css_path
        css_head = '<link href="/css/'
        css_tail = '" rel="stylesheet" type="text/css" media="all">'
        self.css_elem = css_head + self.css_path + css_tail
        self.html_path = html_path
        self.html_link = pc.SITE_URL + "/" + self.html_path.split(os.sep)[-1]
        self.date = date
        self.id_no = 'undefined'
        
    def open_html(self):
        subprocess.run([pc.BROWSER, self.html_path])


    # Assembles Dictionary of Changes For REPLACE_ELEMENT function
    def get_elementary_changes(self):
        changes = {'TITLEBAR': self.title,
                   'CSS': get_css_element(),
                   'TITLEHEAD': self.title,
                   'VERSION': self.version,
                   'BYLINE': self.byline,
                   'SUBTITLE': self.subtitle,
                   'POST': self.post_data}
        return changes

    # Inserts Optional Page Blocks
    def make_optional_changes(self, changes, template):
        global paginate_last_page_switch
        paginate_last_page_switch = False
        for optional in changes:
            if optional == 'IMG':
                while True:
                    img_path = input("\nEnter Path to Image\n> ")
                    if os.path.exists(pc.SITE_PATH + pc.IMG_PATH + img_path):
                        break
                img_path = pc.SITE_PATH + pc.IMG_PATH + img_path
                template = replace_element(template, {'IMG_PATH':img_path})

            if optional == 'ARCHIVE':
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
                template = replace_element(template, {'VERSION': pc.CURRENT_VERSION,
                                                      'TIMESTAMP': get_date()[2],
                                                      'RELEASEUPDATE':
                                                input("\nType a Release Note\n > ")})

            if optional == 'PAGINATION':
                l, d = get_posts(pc.POSTS_DB)
                # Get Previous Link From Last Page
                if len(l) >= 2:
                    prev_page = d[l[-2]]
                    prev_link = d[l[-2]].html_link
                    template = replace_element(template, {'PREV_LINK': prev_link,
                                                          'PREV_NAME': 'PREVIOUS'})
                else: # Remove placeholders if first page
                    template = replace_element(template, {'PREV_LINK': '',
                                                          'PREV_NAME': ''})
                # Open Last Page and Insert Link to Current Page
                if len(l) >= 2:
                    paginate_last_page_switch = True
        return template

    # Get Count of Files in Directory
    def count_posts(self, posts_dir=pc.POSTS_DB):
        pl, _ = get_posts(posts_dir)
        return len(pl)

    # Write HTML to File
    def build_page(self, template):
        if os.path.isdir(pc.HTML_PATH):
            cwd = os.getcwd()
            os.chdir(pc.HTML_PATH)
            # Second Phase is a Rebuild for Pagnation
            if not self.html_path in os.listdir():
                with open(self.html_path, 'w') as fo:
                    fo.write(template)
                    second_phase = False # reset
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
                dict([("ENTRYLINK", d[str(i)].html_link),
                      ("ENTRYNAME", '-'.join(d[str(i)].subtitle.split(' ')).lower()),
                      ("ENTRYDESC", d[str(i)].post_head),
                      ("DATE", d[str(i)].date[2])]))
            # Uses TMP File to Replace Elements with Same Placeholders for Each Post
            with open('archive.tmp', 'w') as temp_file:
                temp_file.write(arc_html.template)
            # Write the Archive Data to the DB for Rebuilding
            with shelve.open(pc.POSTS_DB, writeback=True) as shelf:
                shelf[str(i)].archive_entry = arc_html.template
            # Add the TMP File to a Blank Archive Template in Append Mode
            with open(pc.ARCHIVE_PATH, 'a') as fo:
                fo.write(arc_html.template+"\n")

class Post(Page):
    # Initialize a Regular Post in a TXT File
    def __init__(self, title, byline, version, css_path, html_path, date):
        super().__init__(title, byline, version, css_path, html_path, date)
        self.id_no = self.get_id_no()
        cwd = os.getcwd()
        confirm = input("Write a new post? Y/n? ").lower()
        if confirm.startswith('y'):
            # Check the Paths Are Valid
            if os.path.isdir(pc.TXT_PATH):
                os.chdir(pc.TXT_PATH)
                self.subtitle = input("What is the title of this post?\n")
                # If the TXT File Doesn't Already Exist, Name It by Date
                if not os.path.exists(f"{pc.TXT_PATH}{self.date[0]}.txt"):
                    self.txt_path = f"{pc.TXT_PATH}{self.date[0]}.txt"
                    with open(self.txt_path, 'w') as txt:
                        # Write the title and date of the post
                        txt.write(self.subtitle + "\n")
                        txt.write(self.date[1] + "\n")
                        # Draw a Separating Line Equal to the Length of Heading
                        txt.write("#" * max(len(self.subtitle), len(self.date[1])+2))
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
            # Pretty Sure This Line isn't Necessary, But Will Check Later
            self.post_data = [line for line in self.post_data]
            self.post_data.pop(0) # These Pops Are
            self.post_data.pop(0) # For Removing
            self.post_data.pop(0) # The Heading
            # Then all the lines are joined into one String
            self.post_data = "".join(self.post_data)
            # The first 100 characters of the post are saved for archive preview
            self.post_head = self.post_data.split('\n')[0][:100]

    # The ID_NO is Used to Shelve and Pull Post Objects
    def get_id_no(self, path=pc.TXT_PATH):
        # If ID Hasn't Been Saved...
        if self.id_no == 'undefined':
            # ...Use the Number of TXT Files to Call It
            file_count = len(os.listdir(path))
            return str(file_count + 1)
        else: # Otherwise Return the ID
            return str(self.id_no)

    # With the ID Number, Store the Post Objects in the DB
    def shelve_page(self):
        with shelve.open(pc.POSTS_DB) as shelf:
            shelf[self.id_no] = self

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
def get_css_element():
    head = '<link href="/css/'
    tail = '" rel="stylesheet" type="text/css" media="all">'
    return head + pc.CSS_FILE + tail

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

# Open the Shelf a List and Dict
def get_posts(shelf_database=pc.POSTS_DB):
    with shelve.open(shelf_database) as posts:
        posts_dict = dict(posts)
        posts_list = list(posts_dict.keys())
        posts_list = [int(post) for post in posts_list]
        posts_list.sort() # The List is In Order
        posts_list = [str(post) for post in posts_list]
        return posts_list, posts_dict
    
def paginate_last_page():
    l, d = get_posts(pc.POSTS_DB)
    last_page = d[l[-2]]
    # Used to get Links to Current Page for Last Page
    next_link = d[l[-1]].html_link
    # Opening Last Page
    with open(last_page.html_path) as fo:
        template_lines = fo.readlines()
    # Index Lines for Comment Removal of Next Page Nav Link
    template_lines = [(idx, elem) for idx, elem in enumerate(template_lines)]
    # Search and Replace by Index
    for line in template_lines:
        if line[1].startswith('<!--<a class="next"'):
            template_lines[line[0]] = (line[0], \
                '<a class="next" href="$NEXT_LINK">$NEXT_NAME</a></nav>')
    # Write the lines to temporary file, without indexes
    template_lines = [line[1] for line in template_lines]
    with open("lastpage.html", 'w') as fo:
        for line in template_lines:
            fo.write(line+'\n')
    # Send temp file back through process.
    data = get_html_file("lastpage.html")
    html = make_html_template(data)
    html = replace_element(html, {'NEXT_LINK': next_link,
                                  'NEXT_NAME': 'NEXT'})
    print(html.template)
    rebuild_page(last_page.html_path, html.template)
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
def write_new_post():
    p = Post(*get_page_params())
    p.open_txt()
    p.shelve_page()
    changes = p.get_elementary_changes()
    data = get_html_file()
    html = make_html_template(data)
    html = replace_element(html, changes)
    changes2, removed = select_options()
    html = replace_element(html, changes2)
    html = remove_placeholders(html, removed)
    html = p.make_optional_changes(list(changes2.keys()), html)
    p.build_page(html.template)
    if paginate_last_page_switch:
        paginate_last_page()
    return html, changes, changes2, removed, p


if __name__ == '__main__':
    html, changes, changes2, removed, p = write_new_post()
    

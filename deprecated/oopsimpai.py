import os, sys
import shelve
import subprocess
import random
from datetime import datetime
import pageconfig2 as pc

#class Page:
    #def __init__(self, title, byline, version, css_path, html_path, date):
        #self.title = title
        #self.byline = byline
        #self.version = version
        #self.css_path = css_path
        #self.css_elem = '<link href="/css/' + self.css_path + \
                        #'" rel="stylesheet" type="text/css" media="all">'
        #self.html_path = html_path
        #self.html_link = pc.SITE_URL + "/" + self.html_path.split(os.sep)[-1]
        #self.date = date
        #self.id_no = 'undefined'

    def make_index(self, html_path):
        # TODO
        print("Making this page the index page.")

    #def replace_elements(self, template, element_changes, options):
        #for option in list(options):
            #element_changes.append(options[option])

        #for insert, placeholder in element_changes:
            #for line in template:
                #if line[1] == placeholder:
                    #template[line[0]] = (line[0], insert)
        #return template

    #def build_page(self, template_list):
        #if os.path.isdir(pc.HTML_PATH):
            #os.chdir(pc.HTML_PATH)
            #if not self.html_path in os.listdir():
                #with open(self.html_path, 'w') as fo:
                    #for line in template_list:
                        #fo.write(line[1])
            #else:
                #print("Page Exists. Cannot write file.")
            #os.chdir(cwd)
        #else:
            #print("Give Absolute Path in pageconfig.py for HTML_PATH")
            #sys.exit(1)
        #return self.html_path

    #def select_options(self):
        #self.optional_changes = {'TEMPLATE_RELEASENOTE':
                                    #(pc.TEMPLATE_RELEASENOTE, pc.RELEASENOTE),
                                #'TEMPLATE_ENTRIES':
                                    #(pc.TEMPLATE_ENTRIES, pc.ENTRIES),
                                #'TEMPLATE_FIRSTBLOCK':
                                    #(pc.TEMPLATE_FIRSTBLOCK, pc.FIRSTBLOCK),
                                #'TEMPLATE_PAGINATION':
                                    #(pc.TEMPLATE_PAGINATION, pc.PAGINATION)}
        #for option in list(self.optional_changes):
            #inp = input(f"Add OPTIONAL element for {option}? Y/n\n> ").lower()
            #if inp.startswith('y'):
                #print(f"\tAdding {option}")
            #else:
                #print(f"\tSkipped {option}")
                #del self.optional_changes[option]
        #return self.optional_changes

    def paginate_front_page(self):
        posts_list, posts_dict = get_posts(pc.POSTS_DB)

        if len(os.listdir(pc.TXT_PATH)) >= 3:
            prev_name = posts_dict[posts_list[-1]].subtitle
            prev_link = posts_dict[posts_list[-1]].html_link
        else:
            prev_name = ""
            prev_link = ""
        next_name = "root".upper()
        next_link = pc.SITE_URL

        self.pagin_dict = {'prev_name': (prev_name, "<!-- ,$PREV_NAME(), -->\n"),
                           'prev_link': (prev_link, "<!-- ,$PREV_LINK(), -->\n"),
                           'next_name': (next_name, "<!-- ,$NEXT_NAME(), -->\n"),
                           'next_link': (next_link, "<!-- ,$NEXT_LINK(), -->\n")}

        if len(os.listdir(pc.TXT_PATH)) <= 0:
            del self.pagin_dict['prev_name']
            del self.pagin_dict['prev_link']

        return self.pagin_dict

    def paginate_last_page(last_page):
        posts_list, posts_dict = get_posts(pc.POSTS_DB)



    #def get_element_changes(self, options):
        #self.element_changes =  [(self.title, pc.TITLEBAR),
                            #(self.css_elem, pc.STYLESHEET),
                            #(self.subtitle, pc.SUBTITLE),
                            #(self.title, pc.TITLEHEAD),
                            #(self.version, pc.VERSION),
                            #(self.byline, pc.BYLINE),
                            #(self.post_data, pc.POST),]
        #for option in list(options):
            #self.element_changes.append(options[option])

        #if 'TEMPLATE_PAGINATION' in options.keys():
            #self.pagination_changes = self.paginate_front_page()
            #for change in self.pagination_changes.keys():
                #self.element_changes.append(self.pagination_changes[change])
## TODO
        #if 'TEMPLATE_FIRSTBLOCK' in options.keys():
            #self.img_count = input("How many images will you need? \n> ")
            #pc.TEMPLATE_FIRSTBLOCK *= int(self.img_count)
            #self.rebuild_page()


        return self.element_changes

    def rebuild_page(self):
        self.template_html = get_element_list(self.html_path)
        self.new_html = self.replace_elements(self.template_html,
                                                self.element_changes, {})
        p.build_page(self.new_html)
        subprocess.run([pc.BROWSER, self.html_path])
        return self.template_html



#class Archive(Page):
    #def __init__(self, title, byline, version, css_path, html_path, date):
        #super().__init__(title, byline, version, css_path, html_path, date)

        #def count_posts(self, posts_dir):
            ## TODO
            #print("Counting total posts in posts directory")

        #def get_page_no():
            ## TODO
            #print("Determining number of archiving pages.")


#class Post(Page):
    #def __init__(self, title, byline, version, css_path, html_path, date):
        #super().__init__(title, byline, version, css_path, html_path, date)
        #self.id_no = self.get_id_no()
        #confirm = input("Write a new post? Y/n? ").lower()
        #if confirm.startswith('y'):
            #if os.path.isdir(pc.TXT_PATH):
                #os.chdir(pc.TXT_PATH)
                #self.subtitle = input("What is the title of this post?\n")
                #if not os.path.exists(f"{pc.TXT_PATH}{self.date[0]}.txt"):
                    #self.txt_path = f"{pc.TXT_PATH}{self.date[0]}.txt"
                    #with open(self.txt_path, 'w') as txt:
                        #txt.write(self.subtitle + "\n")
                        #txt.write(self.date[1] + "\n")
                        #txt.write("#" * max(len(self.subtitle), len(self.date[1])+2))
                        #txt.write("\n")
                        #os.chdir(cwd)
                        #return
                #else:
                    #print("File exists. Cannot write new post.")
                    #sys.exit(1)
            #else:
                #print("Check pageconfig.py for an absolute path to dir, TXT_PATH")
                #sys.exit(1)
        #else:
            #sys.exit(1)

    #def open_txt(self):
        #subprocess.run([pc.EDITOR, self.txt_path])
        ## read txt after post is written
        #with open(self.txt_path) as fo:
            #self.post_data = fo.readlines()
            #self.subtitle = self.post_data[0][:-1]
            #self.post_data = [line for line in self.post_data]
            #self.post_data.pop(0)
            #self.post_data.pop(0)
            #self.post_data.pop(0)
            #self.post_data = "".join(self.post_data)

    #def get_id_no(self, path=pc.HTML_PATH):
        #if self.id_no == 'undefined':
            #file_count = len(os.listdir(path))
            #return str(file_count + 1)
        #else:
            #return str(self.id_no)

    #def shelve_page(self):
        #with shelve.open(pc.POSTS_DB) as shelf:
            #shelf[self.id_no] = self



## Get Basic Page Parameters
#def get_title(title=pc.TITLE):
    #return title

#def get_byline(byline=pc.DEFAULT_BYLINE):
    #return byline

#def get_version(version=pc.CURRENT_VERSION):
    #return version

#def get_css_file(css=pc.CSS_FILE):
    #return css

#def get_html_path(path=pc.HTML_PATH):
    #date = get_date()
    #return path + date[0] + ".html"

#def get_date():
    #posted_on = datetime.now().strftime('Posted on %B %d, %Y at %H:%M Hours')
    #timestamp = datetime.now().strftime('%B%d%Y-%H%M').lower()
    #return timestamp, posted_on

#def get_element_list(path="template.html"):
    #with open(path) as fo:
        #template = fo.readlines()
        #return [(idx, elem) for idx, elem in enumerate(template)]

#def get_page_params():
    #title = get_title()
    #byline = get_byline()
    #version = get_version()
    #css_file = get_css_file()
    #html_path = get_html_path()
    #date = get_date()
    #return (title, byline, version, css_file, html_path, date)

#def get_posts(shelf_database):
    #with shelve.open(shelf_database) as posts:
        #posts_dict = dict(posts)
        #posts_list = list(posts_dict.keys())
        #posts_list = [int(post) for post in posts_list]
        #posts_list.sort()
        #posts_list = [str(post) for post in posts_list]
        #return posts_list, posts_dict

def show_posts(attr):
    pl, pd = get_posts(pc.POSTS_DB)
    for idx, post in enumerate(pd.keys(), start=1):
        #try:
        print(str(idx)+") ", f'{pd[post]}.{attr}')
        #except AttributeError:
            #print(str(idx)+") {} not in post".format(attr))

#def make_post():
    #p = Post(*get_page_params())
    #template_html = get_element_list()
    #p.open_txt()
    #initial_options = p.select_options()
    #element_changes = p.get_element_changes(initial_options)
    #html = p.replace_elements(template_html, element_changes, initial_options)
    html_page = p.build_page(html)
    return p

def rebuild_page():
    template_html = get_element_list()
    p.rebuild_page()
    return p

def alias_page(page_obj):
    pa = page_obj
    return pa

def select_images():
    if not imgs:
        imgs = []
    files_in_dir = os.listdir(pc.IMG_PATH)
    total_files = int(len(files_in_dir))
    die_roll = random.randint(1, total_files) - 1
    ballots = [(idx, file) for idx, file in enumerate(files_in_dir)]
    img = print('<img src="{}">'.format(ballots[die_roll][1]))
    imgs = imgs + [img]
    return imgs




#cwd = os.getcwd()
#p = make_post()
#p = rebuild_page()
#p.shelve_page()
#pl, pd = get_posts('posts.db')
#pa = alias_page(p)



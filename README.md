# Senpai Static Page Generator

Simpai is the simple Python static page generator. and it has noticed your need for a hand crafted, statically generated mark up -- but without the tedium of manual maintenance. With Simpai, you will write your HTML template once, format it to be read by Simpai, and it will take care of every page afterwards that you will ever need.

## NEW VERSION: prototype 12/7/2019

So, it's not exactly finished, but it's in working form. 
Features in the new version that the old didn't have:
    
1. Markdown
2. Jinja2 Templating
3. Potentially Easily Custom Designs

I also plan to add a scss compiler, a spellchecker, and some other things.

Ultimately, it will be as feature rich as any other static page generator I've looked at when I'm done with it. At first it will be specifically crafted for `./themes/virulence.factor/` theme: which is a fork of [serenity.scss](https://hale.su/serenity.html) by Lexi Hale and is the the theme I use on [my abandoned github page](virufac.github.io), which maybe will not go abandoned when the finished version is out.

### INSTALLATION

I included a `setup.py` and `requirements.txt` file in the `./setup` directory but I'm not sure how well that works yet. First time designing a package really. 

Ultimately you just need to `pipenv install markdown` and `pipenv install jinja2` (or something similar in a venv of your preference).

===

### start with new_site.py

This is the first script you'll want to touch. Ignore `./example_gen.py`. This will generate an example site directory from `./themes` and `./simpai` and create a file structure for the specific site.
    
`python3 new_site.py example`

There aren't that many methods: 
    
+ `new_site_start(name, root, theme)` -- the only thing you need to specify is `name`, the other positional arguments will default to the only theme that exists right now and to the cwd as the root Simpai directory.
+ `compile_scss(scss)` -- doesn't work yet, but will be added...
+ `copy_python_files(file_to_copy)` takes a list of strings that should correspond to existing files from the `./simapi` package directory.

Overall, this script is a mess that should be cleaned up eventually.

## now you can have a look at example_get.py

This script was written as an example. It is intended that you would write a similar script as this to initialize your site.

```
import example.pagerender as render
import example.pageconfig as c

from simpai.sites import Site
from simpai.data import jdump, jload
```

You'll notice that we are importing some things from the `./simpai` package and other things from the `./example` package, which is just your page data.
But you'll also notice that there are similar files: `render.py` and `config.py`, in the simpai package that you should not be trying to import to adjust your site.
For this reason, they are given the `pagerender` and `pageconfig` variation once in your example site, which you will use that name to import rather than example if you have used something else.

To keep it pretty simple, things that have to do with exactly how your page will be displayed will come from your site directory. Things that have to do with the basic tools of Simpai will come from Simpai.

## methods in ./simpai/sites.py

You'll notice most of the methods I call in the `example_gen.py` file are from the `sites.Sites` class.

+ `site = Site(url, local)` will do `__init__(self, name, url, local=Path.cwd().resolve(), welcome=c.welcome)` -- name and url are all that are important. Note that `c` is how I have imported my `example.pageconfig` module. That file is not very elaborate yet.
+ `site.add_menu_entry(self, name, link, descrip=None, posts=False)` -- posts should be deprecated soon.
+ `site.add_byline(string)` -- a tagline will be added to a list of taglines
+ `site.add_footer_line(self, line, name='main', quip=False)` -- quip clarifies that variant virulence.css class for the p tag, quips. The line is a string and the name defaults to adding to your main category of footer. You'll notice the example on my page has three or four lines, some of them quips and some not. You enter them one after another, in sequence that will be listed in a for loop.
+ `site.add_welcome(self, line, quip=False)` -- works similarly, only lacks the categories. May deprecate those categories or add them later to this.
+ `site.add_author(self, name, email, page)`-- simple, stores about/contact page on the site with email and a name. Will add more options.
+ `site.add_attrs_to_dict(self)` -- this attempts to take all of the site attributes and save them into a dict, for the purposes of serializing into json.... 

### look at ./simpai/data.py another time maybe
All it has right now are `jdump()` and `jload()` methods, although for whatever reason, this is not working yet. Too tired to fix it. It thinks that I'm giving it a PosixPath and will not serialize the dict. 

## Instead look at ./example/pagerender.py

This is more interesting...

```
from jinja2 import Environment, FileSystemLoader
from markdown import markdown
```

Remember, I imported `pagerender` as `render` in the example_gen.py where these are called. The variation is to ensure that you know which (and from where) you are importing in the initiating statements but default back to uniformity.

There are mainly two methods

+ `render.from_jinja2(filename, templates_dir=str(Path().home().joinpath('Projects', 'simpai', 'example', 'templates').resolve()))` -- right now the path is hard coded and will assume you are using the following path... You can adjust this, I will have to fix this, but for now this tests that it works if you reproduce that path or change it in the `pagerender.py` file. The `templates_dir` keywords needs to refer to the entire `./example/templates` directory and everything in it to work. The filename refers to the page you are building right now.
+ `render.from_markdown(md)` -- a fair bit simpler. Returns HTML from markdown input. Will try to interpret `md` as `pathlib.Path` object but if it fails, it will try to concert parameter to `str` and markdown only that.
+ `content()` -- placeholder. Assembles dictionary of keys to be used in jinja templates as names for dynamic values.

The last lines in the `example_gen.py` file say

```
html = render.from_jinja2('index.html')
logging.debug(f"html: {html}, rendered from templates...")

    with open('./example/output/index.html', 'w') as fo:
        fo.write(html)
```

If things are not exactly right, it's a bit finicky, and the hard coding is stupid. But... It does work.

Check your test generated `./example/output/index.html`, which pulls variables from the 

And the next time I work on it, I'll have somewhere to move forward.

This file will at least guide you over how the features will be implemented.

I still need to make templates for all the other types of content the site has.

## I'm considering opening up a project and organizing what needs to be done a little better.

But for now... rest.

# DEPRECATED VERSION: 

I scrapped the original simpai-spg, which you can find in the `/old-version/` directory. At one time it worked in a less complicated form, although I'm not sure if it still works. This deprecated directory is a testament to what this started out as. Very simple. My first project more or less.


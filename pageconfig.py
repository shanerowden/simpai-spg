# viruFac, @shaen@hackers.town
# http://virufac.github.io
# virufac@protonmail.com
# APGL 3.0


# Please use an absolute path in the following two locations:
                # for your txt files, where you will write your posts
POST_PATH = ""

                # for your generated HTML pages, in your local www project
POSTED_PATH = ""


# The following vars can be changed to affect default values directly
# inserted inside of the relevant HTML elements found on any page.
# These default values can be superseded in the replace_element() call
# by passing a different string to its first parameter.

TITLE = "welcome to my new and improved home page"
CURRENT_VERSION = "version 0.4.3.212"
DEFAULT_BYLINE = "Enter a Byline!"
CSS_FILE = "nightblue.css"

# The following are blocks of template HTML which may be included or
# excluded from the generation of any page. The difference between these vars
# and the above is that they are inserts of HTML, not a simple data field.
# You can change them to your liking, but you will need to take into account
# How they fit into the template.html based on their placeholder.... See Below.
# TODO Option to exclude or include not coded.

TEMPLATE_RELEASENOTE = """
<br><h5><div id="updates">You could put just about anything here</div></h5>
<code class="html">
<font family="PT+Sans+Narrow">
<ul><li><b>version 3.0.1</b> -- <b>07/07/2019</b>: <div class="byline">
Page Hand Written and then Effectively Generated into Many Pages with Simpai!"""

# TODO
TEMPLATE_ENTRIES = """
<ul><li><b>Sorted Entries<font size="-1">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[by modified date]</font></b></li><ul>

    <!--start-entry-link-->
<li><a href="/posts/index.html">posts</a>/</li><font size="-1">
<b>--notes-include "... </b> This is going to be a place where I would write something<b>..."</b><br><Br>
    <!-- end-entry-link-->

</ul></ul></div></blockquote><hr>"""

# TODO
TEMPLATE_ENTRY = """
    <!--start-entry-link-->
<li><a href="/posts/index.html">posts</a>/</li><font size="-1">
<b>--notes-include "... </b> This is going to be a place where I would write something<b>..."</b><br><Br>
    <!-- end-entry-link-->"""

TEMPLATE_FIRSTBLOCK = """<code class="html"><p>
    A template page that is merely in a testing phase.
</p></code>"""

TEMPLATE_PAGINATION = """<nav>
<a class="prev" href="/index.html">HERE</a>
<a class="next" href="/index.html">HERE</a>
</nav>"""

# The following are strings representing "variables" which are found on the
# HTML template as a single line. Refer to the example template.html and
# observe how these strings reside on individual lines where blocks of code
# and strings will be filled in their place. Each of these belongs on its
# own line. You may change the values, but you will also need to change the
# template.html -- You can change the variable names if you really want to,
# but you will need to change every appearance of the var name in main.py

STYLESHEET = ",$CSS(),\n"
TITLEBAR = ",$TITLEBAR(),\n"
TITLEHEAD = ",$TITLEHEAD(),\n"
VERSION = ",$VERSION(),\n"
SUBTITLE = ",$SUBTITLE(),\n"
BYLINE = ",$BYLINE(),\n"
FIRSTBLOCK = ",$FIRSTBLOCK(),\n"
POST = ",$POST(),\n"
ENTRIES = ",$ENTRIES(),\n"
RELEASENOTE = ",$RELEASENOTE(),\n"
PAGINATION = ",$PAGINATION(),\n"


# virufacFac, @shaen@hackers.town
# http://virufac.github.io
# virufac@protonmail.com
# APGL 3.0


# The following vars can be changed to affect default values directly
# inserted inside of the relevant HTML elements found on any page.
TITLE = "virufac.github.io"
CURRENT_VERSION = "version 0.9"
DEFAULT_BYLINE = "Grinding Hard on Level 3 Pythons"
CSS_FILE = "random" # File should be kept in /css/ directory


# Please use an absolute path in the following locations:
# Which Should Be in the Same Root Folder for Your Page Gen:
#   DIRECTORY:
ROOT_PATH = "/home/virufac/Git/vfghio-gen/"


#   DIRECTORY: for txt files, where you will write your posts
TXT_PATH = "/home/virufac/Git/vfghio-gen/posts/"


#   FILE: Your main .html Template:
TEMPLATE_FILE = "/home/virufac/Git/vfghio-gen/template.html"


#   FILE: The json database (.json) containing your post data
POSTS_JSON = "/home/virufac/Git/vfghio-gen/posts.json"


# You will need another folder where you website and everything
# that will be uploaded will go:
#   DIRECTORY: The root WWW folder
SITE_PATH = "/home/virufac/Git/virufac.github.io"


#   DIRECTORY: Relative path inside of SITE_PATH:
#       Format like this "/images/"
IMG_PATH = "/img/"


#   DIRECTORY: This is where your HTML files go
HTML_PATH = "/home/virufac/Git/virufac.github.io/posts/"


#   FILE: Archive Template (.html)
ARCHIVE_PATH = "/home/virufac/Git/vfghio-gen/archive.html"


# Your Main Website, including https://
    # URL: No trailing slash:
SITE_URL = "https://virufac.github.io"


# These reflect command line commands for your software of choice
BROWSER = "firefox"
EDITOR = "vim"


# The following are blocks of template HTML which may be included or
# excluded from the generation of any page. The difference between these vars
# and the above is that they are inserts of HTML, not a simple data field.
# You can change them to your liking, but you will need to take into account
# How they fit into the template based on their placeholders...
#    Placeholders are in Caps and begin with $...
#        $LIKETHIS  --  Keep Them Somewhere in the Template Block

TEMPLATE_RELEASENOTE = """
<br><h5><div id="updates">Update and Release Notes</div></h5>
<code class="html">
<font family="PT+Sans+Narrow">
<ul><li><b>$VERSION</b> -- <b>$TIMESTAMP</b>: <div class="byline">
$RELEASEUPDATE
"""

TEMPLATE_ARCHIVE = """
<ul><li><b>Sorted Entries<font size="-1">&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;[by modified date]</font></b></li><ul>
$ARCHIVE_PAGE
</ul></ul></div></blockquote><hr>
"""

TEMPLATE_ENTRY = """
<!--start-entry-link--><li><a href="$ENTRYLINK
">/posts/$ENTRYNAME</a> <font size="-1">($DATE)</font></li>
<b><font size="-1">--post-begins "</b>$ENTRYDESC
<b>..."</font></b><br><Br><!-- end-entry-link-->
"""

TEMPLATE_IMG = """
<code class="html" style="fixed-positioning; max-width="90%;"><p>
<img width="100%" src="$IMG_PATH"></p></code>
"""

TEMPLATE_PAGINATION = """
<nav>
<a class="prev" href="$PREV_LINK">$PREV_NAME</a>
<!--<a class="next" href="$NEXT_LINK">$NEXT_NAME</a>
</nav>-->
"""

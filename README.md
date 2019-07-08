# Simpai version 0.1
Simpai is a Simple Python Static Page Generator. and it has noticed your need for a hand crafted, staticly generated mark up that captures the DIY spirit your personal, hand written HTML page was meant to exuberate without the tedium of manual maintenance. With Simpai, you will write your HTML template once, format it to be read by Simpai, and it will take care of every page afterwards that you will ever need.."

It is currently not quite as developed as tools like Pelican and the like, but in my opinion, it was less overwhelming to simply write this software than to figure out how to make Pelican page look the way I wanted it to.

It's true, this project doesn't even support Markdown yet in your posts, but... it does take your HTML design once formatted and generatre pages for you, inserting your content inside of them. In  the future it will have more features.

## If you're wondering how the program works.. 
I would start by looking at the example template.html page that I use on my own GitHub page, https://virufac.github.io (if you want to see a live version), while simultaneously having a look at the variables in pageconfig.py.

### Known Issues
When you execute main.py from command line, it will ask if you want to create a new page. Currently, 'Y' is the only acceptable answer. 'n' will merely call sys.exit()...

This has not been tested Windows as of yet.

## If you are interested in using this tool but are having trouble with it...
Do not hesitate to contact me. You can find me on the Fediverse @shaen@hackers.town or virufac@protonmail.com

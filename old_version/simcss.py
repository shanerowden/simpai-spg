import os
import simpai
import random

for color in range(0, 360):
    color += 1
    variables = {
        'HUE': color,
        'WIDTH': 35,
        'BRIGHT': str(random.randint(1, 100)) + '%',
        'LINKBR': str(random.randint(1, 100)) + '%',
        'HOVER': str(random.randint(1, 100)) + '%'
        }

    data = simpai.get_html_file('serenity.txt')
    css = simpai.make_html_template(data)
    css = simpai.replace_element(css, variables)

    cwd = os.getcwd()
    os.chdir('css-gen')

    with open('color{}.css'.format(variables['HUE']), 'w') as fo:
        fo.write(css.template)

    os.chdir(cwd)
        

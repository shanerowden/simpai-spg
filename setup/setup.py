from setuptools import setup

setup(name='simpai-spg',
      version='0.2.1',
      description='Simpai is the simple Python static page generator. and it has noticed your need for a hand crafted, statically generated mark up -- but without the tedium of manual maintenance. With Simpai, you will write your HTML template once, format it to be read by Simpai, and it will take care of every page afterwards that you will ever need.',
      url='http://github.com/virufac/simpai-spg',
      author='vF',
      author_email='virufac@protonmail.com',
      license='APGL 3.0',
      packages=['simpai'],
      install_requires=[
          'Jinja2==2.10.3',
          'Markdown==3.1.1',
          'MarkupSafe==1.1.1'
          ]
      zip_safe=False) 

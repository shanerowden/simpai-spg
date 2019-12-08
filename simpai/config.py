from pathlib import Path
import logging


FILE_TREE = {'site_gen': 
                 {'output': {},
                  'templates': {},
                  'css': {}
                  }}

http = "https://"
welcome = ""
content = {'helloworld': 'foobar'}

logging.info(f"simpai.config loaded...")

if __name__ == '__main__':
    print("Not Executable File")

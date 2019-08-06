#!/usr/bin/env python3

import os
import simpai
import pageconfig as pc
import subprocess

if os.path.isdir(pc.HTML_PATH):
    print('')
    print("""WARNING:
    Running this Script Will Delete All Files in...
        "{}"
            ...Before Rebuilding Them.""".format(pc.HTML_PATH))
    
    answer = input("\n\tProceed? Y/n? ").lower()
            
    if answer.startswith('y'):
        os.chdir(pc.HTML_PATH)
        files = os.listdir()

        for f in files:
            print("Removing {}".format(f))
            subprocess.run(['rm', f])
        
        jdata = simpai.load_json()
        first_post = list(jdata.keys())[0]
        last_post = list(jdata.keys())[-1]

        for post in jdata.keys():
            print("Rebuilding #{}: {}".format(post, jdata[post]['html_path']))
            
            first_changes = {
                'TITLEBAR': jdata[post]['title'],
                'TITLEHEAD': jdata[post]['title'],
                'VERSION': jdata[post]['version'],
                'BYLINE': jdata[post]['byline'],
                'SUBTITLE': jdata[post]['subtitle'],
                'POST': jdata[post]['post_data'],
                'CSS': jdata[post]['css_elem']
                }
            
            first_optional = dict()
            second_changes = dict()
            removal_list = []
            
            if jdata[post]['option_img']:
                first_optional['IMG'] = pc.TEMPLATE_IMG
                second_changes['IMG_PATH'] = jdata[post]['img_path']
            else:
                removal_list.append('IMG')
            
            if jdata[post]['option_archive']:
                first_optional['ARCHIVE'] = pc.TEMPLATE_ARCHIVE
                with open(pc.ARCHIVE_PATH, 'r') as fo:
                    arc_html = fo.read()
                second_changes['ARCHIVE_PAGE'] = arc_html
            else:
                removal_list.append('ARCHIVE')
                
            if jdata[post]['option_releasenote']:
                first_optional['RELEASENOTE'] = pc.TEMPLATE_RELEASENOTE
                second_changes['RELEASEUPDATE'] = jdata[post]['releasenote']
                second_changes['VERSION'] = jdata[post]['version']
                second_changes['TIMESTAMP'] = jdata[post]['date'][2]
            else:
                removal_list.append('RELEASENOTE')
                
            if jdata[post]['option_pagin']:
                first_optional['PAGINATION'] = pc.TEMPLATE_PAGINATION
                prev_link = jdata[post].get('prev_link', '')
                next_link = jdata[post].get('next_link', '')
                second_changes['PREV_LINK'] = prev_link
                second_changes['NEXT_LINK'] = next_link
                second_changes['NEXT_NAME'] = 'NEXT'
                second_changes['PREV_NAME'] = 'PREVIOUS'
                
                if first_post == post:
                    del second_changes['PREV_LINK']
                    del second_changes['PREV_NAME']
                    removal_list.append('PREV_LINK')
                    removal_list.append('PREV_NAME')
                if last_post == post:
                    del second_changes['NEXT_LINK']
                    del second_changes['NEXT_NAME']
                    removal_list.append('NEXT_LINK')
                    removal_list.append('NEXT_NAME')
                                        

            else:
                removal_list.append('PAGINATION')
                
            html_data = simpai.get_html_file()
            template_html = simpai.make_html_template(html_data)
            changed_html = simpai.replace_element(template_html, first_changes)
            changed_again_html = simpai.replace_element(changed_html, first_optional)
            
            #INSERT REMOVE COMMENTS FROM NEXT LINK
            
            template_lines = changed_again_html.template.split('\n')
            template_lines = [(idx, elem) for idx, elem in enumerate(template_lines)]

            for line in template_lines:
                if line[1].startswith('<!--<a class="next"'):
                    template_lines[line[0]] = (line[0], \
                        '<a class="next" href="$NEXT_LINK">$NEXT_NAME</a></nav>')
                    
            template_lines = [line[1] for line in template_lines]
            
            template_string = '\n'.join(template_lines)
            changed_back_html = simpai.make_html_template(template_string)
        
            final_html = simpai.replace_element(changed_back_html, second_changes)
            final_final_html = simpai.remove_placeholders(final_html, removal_list)
            
            template_lines = final_final_html.template.split('\n')
            template_lines = [(idx, elem) for idx, elem in enumerate(template_lines)]
            
            for line in template_lines:
                if line[1] == '<a class="next" href=""></a></nav>':
                    template_lines[line[0]] = (line[0], '')
                if line[1] == '<nav><a class="prev" href=""></a>':
                    template_lines[line[0]] = (line[0], '')
                    
            template_lines = [line[1] for line in template_lines]
            
            template_string = '\n'.join(template_lines)
            finnal_final_final_html = simpai.make_html_template(template_string)
            
            with open(jdata[post]['date'][0] + '.html', 'w') as fo:
                fo.write(finnal_final_final_html.template)
        
else:
    print("pageconfig file needs HTML_PATH to website's posts directory")
                
                
                
                
                
                
                
                
                
                

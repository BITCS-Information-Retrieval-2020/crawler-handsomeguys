import jsonlines
import json
import re

def format_title(title):
    # title = re.sub(r'Session\s*\w+\s*-\s*', '', title)
    # title = re.sub(r'SIGIR\s*\w*\s*-\s*', '', title)
    # title = re.sub(r'\[[\x00-\x7F]+?]\s*', '', title)  # 去掉中括号
    # title = re.sub(r'(\([\x00-\x7F]*?\))', '', title)  # 去掉小括号
    title = re.sub(r'[A-Z][A-Z]+(\-[A-Z]+)?(\s|\')?([0-9]{2,4}|paper)(\soral\spaper)?','~',title)
    title = re.sub(r'(Teaser|(short\s)?presentation|10m\stalk|Oral|Spotlight|Presentation|Talk|OralPresentation|Pitch\sVideo)','~',title)
    title = re.sub(r'([\|\-\—\:,]\s?~|~\s?[\|\—\-\:,]|~\s?[\|\—\-\:,]\s?~)','~',title)
    title = re.sub(r'~.*?~','',title)
    title = re.sub(r'~','',title)
    # title = re.sub(r'oral\spaper','',title)
    title = title.strip()
    return title

format_title('ICRA2020 online presentation: Integrated Motion Planner for Real-time Aerial Videography')
with open('example.txt','r') as f:
    with open('result.json','w') as j:
        t = f.readlines()
        for each_sentence in t:
            temp_result = {
                'result':format_title(each_sentence),
            }
            temp_source = {
                'source':each_sentence
            }
            json.dump(temp_source,j,ensure_ascii=False)
            j.write('\n')
            json.dump(temp_result,j,ensure_ascii=False)
            j.write('\n')
            j.write('\n')
    #    reader = jsonlines.Reader(f)
    #    for instance in reader:
              
# m = format_title('[ECCV 2020 Workshop] Long-term Object Tracking (RLT-DiMP) [full ver.]')
# print(m)
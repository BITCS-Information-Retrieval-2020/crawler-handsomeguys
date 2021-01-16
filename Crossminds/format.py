import json
import re


def format_title(title):
    title = re.sub(r'Session\s*\w+\s*-\s*', '', title)
    title = re.sub(r'SIGIR\s*\w*\s*-\s*', '', title)
    title = re.sub(r'\[[\x00-\x7F]+?]\s*', '', title)  # 去掉中括号
    title = re.sub(r'(\([\x00-\x7F]*?\))', '', title)  # 去掉小括号
    title = re.sub(r'[A-Z][A-Z]+(\-[A-Z]+)?(\s|\')?([0-9]{2,4}|paper)(\soral\spaper)?', '~', title)
    title = re.sub(r'(Teaser|(short\s)?presentation|10m\stalk|Oral|Spotlight|Presentation|Talk|OralPresentation|Pitch\sVideo)', '~', title)
    title = re.sub(r'([\|\-\—\:,]\s?~|~\s?[\|\—\-\:,]|~\s?[\|\—\-\:,]\s?~)', '~', title)
    title = re.sub(r'~.*?~', '', title)
    title = re.sub(r'~', '', title)
    # title = re.sub(r'oral\spaper','',title)
    title = title.strip()
    return title

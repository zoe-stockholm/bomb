import re


def remove_tags(text):
    if isinstance(text, str):
        p = re.compile(r'<.*?>')
        return p.sub('', text)
    else:
        return text
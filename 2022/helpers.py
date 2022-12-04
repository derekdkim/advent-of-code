# Snippet for parsing contiguous numbers with regex
import re

num_regex = "\d+"


def regex_parse(pattern, str):
    content = [int(x) for x in re.findall(pattern, str)]
    print(content)

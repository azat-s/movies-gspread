import re

def print_divider():
    print('')
    print('===========================')

def ask(question):
    answer = input(question).lower()
    return answer == 'y' or answer == 'yes'

def without_starting_the(title):
    the_re = re.compile(r'The\s')
    has_the = bool(re.match(the_re, title))
    if has_the:
        title = title.replace('The ', '', 1)

    return (title, has_the)

def handle_the(title):
    title, has_the = without_starting_the(title)
    if has_the:
        title += ', The'
    
    return title
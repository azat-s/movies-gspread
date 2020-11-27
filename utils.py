import re
import enquiries
from datetime import datetime

def print_divider():
    print('')
    print('===========================')

def ask(question):
    print(question)
    answer = input('[↩ / n] > ').lower()
    return answer == ''

def add_fav(viewer):
    question = f"Mark it as {viewer}'s favorite?"
    options = ['Yes', 'No']
    choice = enquiries.choose(question, options)
    return choice

def rate(viewer):
    question = f'{viewer}, how did you like this movie/show?'
    didnt = "Didn't watch it"
    options = ['10', '9', '8', '7', '6', '5', '4', '3', '2', '1', '0', didnt]
    rating = enquiries.choose(question, options)
    if rating == didnt:
        return None
    return rating

def watched_on(viewer):
    question = f"Did {viewer} watch it today?"
    today = 'Today'
    options = [today, 'Another date']
    day = enquiries.choose(question, options)
    if day == today:
        return datetime.today().strftime('%d.%m.%Y')
    else:
        return input(f'Please enter the date, {viewer}. (dd.mm.yyyy) > ')



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
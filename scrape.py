import requests
from bs4 import BeautifulSoup
import re
from utils import print_divider

def get_movie_data(url):
  print_divider()
  print('Scraping IMDB ...')
  r = requests.get(url)
  soup = BeautifulSoup(r.text,  'html.parser')

  data = []

  title_html = soup.find('div', { 'class' : 'titleBar'}).find('h1')
  title = title_html.contents[0].replace(u'\xa0', u'').strip()
  data.append(title)

  date_html = soup.find('div', { 'class' : 'titleBar'}).find_all('a')[-1]
  date_text = date_html.get_text().replace(u'\xa0', u'').strip() 
  years = re.search(r'\d{4}–*\d*', date_text).group()
  data.append(years)
  
  creators_html = soup.find('div', { 'class': 'credit_summary_item' }).find_all('a')
  creators_list = []

  for a in creators_html:
    creators_list.append(a.get_text().replace(u'\xa0', u'').strip())

  creators = ", ".join(creators_list)
  data.append(creators)

  print_divider()
  print('Here is what I found:')
  print('Title: ' + data[0])
  print('Years: ' + data[1])
  print('Creators: ' + data[2])

  return data

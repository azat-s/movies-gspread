import gspread
from oauth2client.service_account import ServiceAccountCredentials
import re
from datetime import datetime
from scrape import get_movie_data
from utils import print_divider
from utils import ask
from utils import handle_the
from utils import without_starting_the

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

credentials = ServiceAccountCredentials.from_json_keyfile_name('credentials.json', scope)
gc = gspread.authorize(credentials)

ss = gc.open("movie_ratings")
worksheet = ss.get_worksheet(0)

print_divider()
url = input('Please provide the imdb link > ')
sheet_row = get_movie_data(url)

viewers = ['Aya', 'Azat']

for viewer in viewers:
  print_divider()
  watched = ask(f'Did {viewer} watch it? (y/n) > ')
  if watched:
    rating = input(f"What is {viewer}'s rating? (0-10) > ")
    sheet_row.append(rating)
    is_fav = input(f"Mark it as {viewer}'s favorite? (Yes/No) > ")
    sheet_row.append(is_fav)
    watched_today = ask(f"Did {viewer} watch it today? (y/n) > ")
    if watched_today:
      sheet_row.append(datetime.today().strftime('%d.%m.%Y'))
    else:
      watch_date = input(f'Please enter the date for {viewer}. (dd.mm.yyyy) > ')
      sheet_row.append(watch_date)
  else:
    sheet_row.append("")
    sheet_row.append("")
    sheet_row.append("")

print_divider()
print("Here is the result:")
print(sheet_row)

already_exists = False

title = sheet_row[0]
years = sheet_row[1]

sheet_row[0] = handle_the(sheet_row[0])

title_re = re.compile(without_starting_the(title)[0], re.I)
matched_titles_cell_list = worksheet.findall(title_re)

existing_row = None
existing_row_number = None

for cell in matched_titles_cell_list:
  if already_exists:
    break
  existing_row_number = cell.row
  existing_row = worksheet.row_values(cell.row)
  existing_years = existing_row[1]
  pattern_years = re.compile(years[:4])
  same_year = bool(re.match(pattern_years, existing_years))
  already_exists = same_year

if already_exists:
  print_divider()
  print('It seems this title already exists. Take a look.')
  print(existing_row)
  update_both = ask('Update the row? (y/n) > ')
  if update_both:
    print_divider()
    print('Updating Google Sheets ...')
    worksheet.update(f'A{existing_row_number}:I{existing_row_number}', [sheet_row])
    print('Updated!')
    # TODO: Update only one viewer
  else:
    print('Quit without changing anything!')
else:
  print_divider()
  print('Uploading to google sheets ...')
  worksheet.append_row(sheet_row)
  print('Done!')

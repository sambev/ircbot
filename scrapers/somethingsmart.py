#def somethingSmart():
"""
get a random item from wikipedia's common misconception page
@return trivia: String with description, link to anchor in article
"""
import requests
import json
import random
from bs4 import BeautifulSoup

# Get the page contents and make a soup object from it
page = requests.get('http://en.wikipedia.org/wiki/Monty_Python')
the_html = BeautifulSoup(page.text)

main_div = the_html.find_all('h3', 'mw-content-text')[0]

print main_div
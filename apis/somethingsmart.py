#def somethingSmart():
"""
get a random item from wikipedia's common misconception page
@return trivia: String with description, link to anchor in article
"""
import requests
import json
import random
from bs4 import BeautifulSoup
import mwlib

# Get the page contents and make a soup object from it
r = requests.get('http://en.wikipedia.org/w/api.php?action=query&pageids=321956&redirects&format=json&export&exportnowrap')

# grab the xml from the results
xml_soup = BeautifulSoup(r.text, 'xml')

# pull the wiki text out
text_dump = xml_soup.find('text').text

# split the wiki text into an array
text_array = text_dump.split('\n')

# choose a random item to display
random_item = random.randint(0,len(text_array)-1)


print text_array[random_item]
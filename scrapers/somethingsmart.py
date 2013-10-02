#def somethingSmart():
"""
get a random item from wikipedia's common misconception page
@return trivia: String with description, link to anchor in article
"""
import requests
import json
import random

# Get the page contents and make a soup object from it
r = requests.get('http://en.wikipedia.org/w/api.php?action=query&pageids=321956&redirects&format=json&export')
print r.json()

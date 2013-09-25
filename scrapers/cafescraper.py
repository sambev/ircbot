def scrapeCafe():
	"""
	Scrape the EastBay Cafe's site for the current lunch menu
	"""
	from bs4 import BeautifulSoup
	import requests

	# Get the page contents and make a soup object from it
	page = requests.get('http://www.eastbaycafe.com/menu.php')
	the_html = BeautifulSoup(page.text)

	mapping = {
	    'soup': 'steam',
	    'flavor': 'flavor',
	    'main': 'mainevent',
	    'greens': 'fieldofgreens',
	    'grill': 'dailygrill',
	}

	stations = {}
	main_div = the_html.find_all('div', 'menu_content')[0]

	# For each mapping, find the Menu Item
	# thanks to iffycan for the more elegant approach
	for k,v in mapping.items():
	    try:
	        stations[k] = main_div.find_all('li', v)[0].contents[2].get_text()
	    except:
	    	stations[k] = 'Not listed'
	        pass

	return stations
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
	    'Steam \'n Turren': 'steam',
	    'Flavor & Fire': 'flavor',
	    'Main Event': 'mainevent',
	    'Field Of Greens': 'fieldofgreens',
	    'The Grillery': 'dailygrill',
	}

	menu = {
		'item_max_width': 0,
		'station_max_width': 0,
		'stations': {}
	}
	main_div = the_html.find_all('div', 'menu_content')[0]

	# For each mapping, find the Menu Item
	# thanks to iffycan for the more elegant approach
	for k,v in mapping.items():
	    try:
	    	li = main_div.find_all('li', v)[0];
	    	menu_item = li.find_all('em')[0].get_text()
        	prices = li.find_all('strong')
	        if v == 'steam':
	        	price = "%s Cup / %s Bowl" % (prices[0].get_text().lstrip('/ '), prices[1].get_text().lstrip('/ '))
	        else:
	        	price = prices[0].get_text().lstrip('/ ')
	        menu['item_max_width'] = max(menu['item_max_width'], len(menu_item))
	        menu['station_max_width'] = max(menu['station_max_width'], len(k))
	        menu['stations'][k] = {
	        	'item': menu_item,
	        	'price': price
	        }
	    except:
	    	menu['stations'][k] = None
	        pass

	return menu
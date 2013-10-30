def quote():	
    """
    Gets a random quote from the quotes subreddit
    @return response dictionary 
    """
    import requests
    import json
    from random import randint

    # send the request and get the data
    r = requests.get('http://www.reddit.com/r/quotes.json')

    data = json.loads(r.text)
    response = ""
    if data['data']:
    	i = randint(0,len(data['data']['children']))
        response = data['data']['children'][i]['data']['title']
    else:
        response = None

    return response
        

if __name__ == "__main__":
    print quote()
import requests
import json

def getSubReddit(query, count):
    """
    Gets the top <count> number of stories on reddit for a given subreddit 
    @return response dictionary list 
    """

    # send the request and get the data
    r = requests.get('http://www.reddit.com/r/%s.json?limit=%s' % (query, count))

    try:
        data = json.loads(r.text)
    except ValueError:
        return None
    responses = {}

    if 'data' in data:
        for i in xrange(0,count):
            responses[i] = {
                'title':data['data']['children'][i]['data']['title'],
                'permalink':data['data']['children'][i]['data']['permalink'],
                'url':data['data']['children'][i]['data']['url']
            }
    else:
        responses = None

    return responses

       
def getQuote():    
    """
    Gets a random quote from the quotes subreddit
    @return response dictionary 
    """
    from random import randint

    # send the request and get the data
    r = requests.get('http://www.reddit.com/r/quotes.json?limit=100')

    try:
        data = json.loads(r.text)
    except ValueError:
        return None

    if 'data' in data:
        i = randint(0,len(data['data']['children'])-1)
        response = data['data']['children'][i]['data']['title']
    else:
        response = None

    return response
        


if __name__ == "__main__":
    import sys
    query = sys.argv[1]    
    count = int(sys.argv[2])
    print reddit(query, count)
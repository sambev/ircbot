import requests
import json

def getSubReddit(query, count):
    """
    Gets the <count> story on reddit for a given subreddit <query>
    @return response dictionary item 
    """

    # send the request and get the data
    r = requests.get('http://www.reddit.com/r/%s.json?limit=%s' % (query, count))

    try:
        data = json.loads(r.text)
    except ValueError:
        return None

    count = count - 1
    if 'data' in data:
        response = {
            'title':data['data']['children'][count]['data']['title'],
            'permalink':data['data']['children'][count]['data']['permalink'],
            'url':data['data']['children'][count]['data']['url']
        }
    else:
        response = None

    return response

       
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
    print getSubReddit(query, count)
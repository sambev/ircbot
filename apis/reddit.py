def reddit(query, count):
    """
    Gets the top <count> number of stories on reddit for a given subreddit 
    @return response dictionary list 
    """
    import requests
    import json

    # send the request and get the data
    r = requests.get('http://www.reddit.com/r/%s.json?limit=%s' % (query, count))

    data = json.loads(r.text)
    responses = {}
    if data['data']:
        for i in xrange(0,count):
            responses[i] = {
                'title':data['data']['children'][i]['data']['title'],
                'permalink':data['data']['children'][i]['data']['permalink'],
                'url':data['data']['children'][i]['data']['url']
            }
    else:
        responses = None

    return responses
        

if __name__ == "__main__":
    import sys
    query = sys.argv[1]    
    count = int(sys.argv[2])
    print reddit(query, count)
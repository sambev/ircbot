def urbanDict(query):
    """
    Searches urbandictionary.com for a definition to the query given
    @return response dictionary 
    """
    import requests
    import json

    # send the request and get the data
    r = requests.get('http://api.urbandictionary.com/v0/define?term=%s' % (query))
    data = json.loads(r.text)

    if data['list']:
        response = {
            'definition':data['list'][0]['definition'].encode('utf-8'),
            'example':data['list'][0]['example'],
            'permalink':data['list'][0]['permalink']
        }
    else:
        response = None

    return response
        

if __name__ == "__main__":
    import sys
    query = sys.argv[1]
    urbandic(query)
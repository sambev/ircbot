import requests
from bs4 import BeautifulSoup

def getCurrentSong(username):
    """
    Get the current song that <username> is listening to
    @param: username (string)
    @returns: song (string)
    """
    r = requests.get('http://ws.audioscrobbler.com/1.0/user/%s/recenttracks.rss' % username)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text)
        return soup.item.title.string


if __name__ == '__main__':
    import sys
    print getCurrentSong(sys.argv[1])

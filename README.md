ircbot
======

IRC bot in Twisted

See requirements.txt for... the requirements.  The easiest way to install them is with pip.  Built using python 2.7.3.

Setup instructions:

1. Install dependencies with `pip install -r requirements.txt`
2. create a config.cfg file for your wolfram keys
3. create a files directory with messages.json and user_info.json inside of it.


If you don't have pip, use easy install or apt-get to get it

### Ubuntu/Debian Installation:

You will probably need the libxml2-dev and libxslt-dev packages (for BeautifulSoup, used for scrapers). 

`apt-get install libxml2-dev libxslt-dev`

### Mac Installation:

You will need Xcode with commandline tools installed and (probably?) the libxml packages mentioned above


### Windows Installation:

If you get it running on windows and have easy to follow steps, feel free to udpate this.

### Basic usage:
`python AL.py <server> <port> <channel> <logfile>`



ircbot
======

IRC bot in Twisted

See requirements.txt for... the requirements.  The easiest way to install them is with pip.
Built using python 2.7.3.

### Ubuntu/Debian Installation:

You will probably need the libxml2-dev and libxslt-dev packages (for BeautifulSoup, used for scrapers). 

`apt-get install libxml2-dev libxslt-dev`

Then you can run this:

`pip install -r requirements.txt`

If you don't have pip use easy install or apt-get to get it

`easy install pip`
`apt-get install python-pip`


### Mac Installation:

You will need Xcode with commandline tools installed and (probably?) the libxml packages mentioned above

Then run the pip command:

`pip install -r requirements.txt`

If you don't have pip, use easy_install to install it

`easy_install pip`


### Windows Installation:

If you get it running on windows and have easy to follow steps, feel free to udpate this.

### Basic usage:
`python AL.py <server> <port> <channel> <logfile>`



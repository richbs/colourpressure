colourpressure
==============

Extract image palette from images and chuck onto STDOUT


1. `wget http://www.ijg.org/files/jpegsrc.v7.tar.gz`
1. `tar xvzf jpegsrc.v7.tar.gz`
1. `cd jpeg-7`
1. `./configure && make`
1.  `sudo make install`
1. `sudo easy_install pip`
1. `sudo pip install virtualenv`
1. `git clone git@github.com:richbs/colourpressure.git`
1. `cd colourpressure`
1. `pip install --upgrade -r requirements.txt`
1. `python ./colourpressure.py image.jpeg`
`# show approximate terminal colours`
1. `python ./colourpressure.py -v image.jpeg`

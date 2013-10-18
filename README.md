# Stats-Simple

## Server monitoring for programmers, by programmers

### Usage

#### 1. Get the code

Get a zip from github, or if you've got git installed:

    git clone https://github.com/danwinkler/stats-simple.git

from the command line.

#### 2. Setup the config files

You should see two folders, node and server.

The server runs on a machine reachable from every node. Copy over the templates before you edit the config:

    cd server
    cp server.cfg.template server.cfg
    cp db.db.template db.db

The node runs on every machine you want to monitor (including the machine running the server if you want). 
Again copy over the template:

    cd node
    cp node.cfg.template node.cfg

The config files are straight-forward json blocks, see [the wiki](https://github.com/danwinkler/stats-simple/wiki) 
for detailed info.

#### 4. Install dependencies

Everything is python, so that's got to be installed on every machine. (Tested with 2.7)

Server Specific Dependencies:

None!

Node Specific Dependencies:

The default collectors require [psutil](https://code.google.com/p/psutil/), and [requests](http://www.python-requests.org/) (included), but if you don't use them, there are no dependencies.

#### 4. Run the code
For the server (from the server folder):

    python server.py

For the nodes (from the node folder):

    python node.py


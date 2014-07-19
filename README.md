Install
=======

Step 1:
-------

```
$ mkdir nashboard.com
$ cd nashboard.com
$ git clone git@bitbucket.org:mahendrakalkura/nashboard.com.git .
```

Step 2:
-------

```
$ mkvirtualenv nashboard.com
$ workon nashboard.com
$ pip install -r requirements.txt
$ cp settings.py.sample settings.py # Line 10
$ deactivate
```

Step 3:
-------

```
$ npm install -g bower
$ bower install
```

Assets
======

```
$ workon nashboard.com
$ python manager.py assets_
$ deactivate
```

Twitter
=======

```
$ workon nashboard.com
$ python manager.py twitter_
$ deactivate
```

Server
======

```
$ workon nashboard.com
$ python server.py
$ deactivate
```

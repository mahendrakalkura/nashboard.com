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
$ cp settings.py.sample settings.py
$ deactivate
```

Step 3:
-------

```
$ npm install -g bower
$ bower install
```

Step 4:
-------

```
mysql nashboard.com < files/0.sql
mysql nashboard.com < files/1.sql
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

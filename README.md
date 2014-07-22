Install
=======

Step 1:
-------

```
$ git clone git@bitbucket.org:mahendrakalkura/nashboard.com.git .
$ cd nashboard.com
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
add local server configuration info into `settings.py`

Step 3:
-------

```
$ npm install -g bower
$ bower install
$ npm install -g less
```

Step 4:
-------

```
$ mysql
mysql> create database nashboard;
$ mysql nashboard < files/0.sql
$ mysql nashboard < files/1.sql
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

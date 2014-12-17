Install
=======

Step 1:
-------

```
$ cd nashboard.com
$ git clone git@bitbucket.org:bearcott/nashboard.com.git .
```

Step 2:
-------

```
$ cd nashboard.com
$ mkvirtualenv nashboard.com
$ pip install -r requirements.txt
$ cp settings.py.sample settings.py
$ deactivate
```

Step 3:
-------

```
$ cd nashboard.com
$ npm install -g bower
$ npm install -g less
$ bower install
```

Step 4:
-------

```
$ cd nashboard.com
$ mysql -e 'CREATE DATABASE `nashboard.com`'
$ mysql nashboard.com < files/0.sql
$ mysql nashboard.com < files/1.sql
$ mysql nashboard.com < files/2.sql
$ mysql nashboard.com < files/3.sql
$ mysql nashboard.com < files/4.sql
```

Assets
======

```
$ cd nashboard.com
$ workon nashboard.com
$ python manager.py assets_
$ deactivate
```

Others
======

crontab
-------

```
0 * * * * cd {{ path }}/scripts && {{ virtualenv }}/python manager.py process_1
0 * * * * cd {{ path }}/scripts && {{ virtualenv }}/python manager.py process_2
```

supervisor
----------

```
# nashboard.com_twitter.conf
[program:nashboard.com_twitter]
autorestart=true
autostart=true
command={{ virtualenv }}/celery worker --app=manager --concurrency=50 --loglevel=WARNING --pool=prefork
directory={{ path }}
group={{ group }}
redirect_stderr=true
startsecs=0
user={{ user }}
```

```
# nashboard.com_uwsgi.conf
[program:nashboard.com_uwsgi]
autorestart=true
autostart=true
command=uwsgi --yaml nashboard.com_uwsgi.yaml
directory={{ path }}
group=ubuntu
redirect_stderr=true
startsecs=0
user=ubuntu
```

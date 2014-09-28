# -*- coding: utf-8 -*-

from contextlib import closing
from datetime import datetime, timedelta
from random import choice, randint
from urlparse import urlparse

from furl import furl
from requesocks import get
from requesocks.exceptions import (
    ConnectionError,
    HTTPError,
    RequestException,
    TooManyRedirects,
    URLRequired,
)
from requesocks.packages.urllib3.packages.socksipy.socks import Socks5Error
from scrapy.selector import Selector
from simplejson import loads
from simplejson.scanner import JSONDecodeError

from modules import database
from modules import log
from modules import models
from modules import utilities


def process():
    with closing(database.session()) as session:
        for handle in session.query(models.handle).order_by('id asc').all():
            seven_days_ago = datetime.now() - timedelta(days=7)
            log.write(10, handle.name, 1)
            tweets = []
            if not tweets:
                tweets = get_tweets('from:@%(name)s' % {
                    'name': handle.name,
                })
            if not tweets:
                tweets = get_tweets(handle.name)
            for tweet in tweets:
                if tweet['text'].startswith('@'):
                    continue
                if tweet['text'].startswith('I posted'):
                    continue
                if utilities.is_retweet(tweet['text']):
                    continue
                if tweet['created_at'] <= seven_days_ago:
                    continue
                if tweet['user_name'] == handle.name:
                    instance = session.query(models.tweet).get(tweet['id'])
                    if not instance:
                        instance = models.tweet(**{
                            'id': tweet['id'],
                        })
                    instance.handle = handle
                    instance.created_at = tweet['created_at']
                    instance.media = tweet['media']
                    instance.text = tweet['text']
                    session.add(instance)
                    session.commit()
                    handle.profile_image_url = tweet['user_profile_image_url']
                    handle.screen_name = tweet['user_screen_name']
                    session.add(handle)
                    session.commit()
                    session.refresh(handle)
            log.write(10, len(tweets), 2)
        session.query(models.tweet).filter(
            models.tweet.created_at <= seven_days_ago
        ).delete(synchronize_session=False)
        session.commit()


def get_tweets(q):
    tweets = []
    params = {
        'composed_count': '0',
        'f': 'realtime',
        'include_available_features': '0',
        'include_entities': '0',
        'include_new_items_bar': 'false',
        'interval': '30000',
        'latent_count': '0',
        'q': q,
        'scroll_cursor': '',
        'src': 'typd',
    }
    url = 'https://twitter.com/i/search/timeline'
    referer = urlparse(furl(url).add({
        'f': 'realtime',
        'q': q,
        'src': 'typd',
    }).url)
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'identity, deflate, compress, gzip',
        'referer': '%(path)s?%(query)s' % {
            'path': referer.path,
            'query': referer.query,
        },
        'user-agent': get_user_agent(),
        'x-requested-with': 'XMLHttpRequest',
        'x-twitter-polling': 'true',
    }
    while True:
        try:
            response = get(
                'https://twitter.com/i/search/timeline',
                headers=headers,
                params=params,
                proxies={
                    'http': 'socks5://72.52.91.120:%(port)d' % {
                        'port': (9050 + randint(1, 50)),
                    },
                    'https': 'socks5://72.52.91.120:%(port)d' % {
                        'port': (9050 + randint(1, 50)),
                    },
                },
                timeout=60.00
            )
        except (
            ConnectionError,
            HTTPError,
            RequestException,
            Socks5Error,
            TooManyRedirects,
            URLRequired,
        ):
            break
        try:
            contents = loads(response.text)
        except (JSONDecodeError, TypeError, ValueError):
            break
        if not contents:
            break
        if not 'items_html' in contents:
            break
        for tweet in Selector(
            text=contents['items_html']
        ).xpath(
            '//div[@data-tweet-id]'
        ):
            tweet = get_tweet(tweet)
            if tweet:
                tweets.append(tweet)
        if len(tweets) >= 500:
            break
        if not contents['has_more_items']:
            break
        if 'scroll_cursor' in contents:
            params['scroll_cursor'] = contents['scroll_cursor']
    return tweets


def get_tweet(tweet):
    id = ''
    created_at = ''
    media = ''
    text = ''
    user_name = ''
    user_profile_image_url = ''
    user_screen_name = ''
    try:
        id = tweet.xpath('.//@data-tweet-id').extract()[0]
    except IndexError:
        pass
    try:
        created_at = datetime.fromtimestamp(int(tweet.xpath(
            './/div[@class="content"]/div[@class="stream-item-header"]/'
            'small[@class="time"]/a/span/@data-time'
        ).extract()[0]))
    except IndexError:
        pass
    try:
        media = Selector(text=tweet.xpath(
            './/@data-expanded-footer'
        ).extract()[0]).xpath('.//img/@src').extract()[0]
    except IndexError:
        pass
    try:
        text = tweet.xpath(
            './/div[@class="content"]/p[@class="js-tweet-text tweet-text"]'
        ).xpath(
            'string()'
        ).extract()[0].strip()
    except IndexError:
        pass
    try:
        user_name = tweet.xpath('.//@data-screen-name').extract()[0]
    except IndexError:
        pass
    try:
        user_profile_image_url = tweet.xpath(
            './/div[@class="content"]/div[@class="stream-item-header"]/a/img/'
            '@src'
        ).extract()[0]
    except IndexError:
        pass
    try:
        user_screen_name = tweet.xpath('.//@data-name').extract()[0]
    except ValueError:
        pass
    if (
        created_at
        and
        id
        and
        (
            text
            and
            (
                not text.startswith('http')
                or
                ' ' in text
            )
        )
        and
        user_name
        and
        user_profile_image_url
        and
        user_screen_name
    ):
        return {
            'created_at': created_at,
            'id': id,
            'media': media,
            'text': text,
            'user_name': user_name,
            'user_profile_image_url': user_profile_image_url,
            'user_screen_name': user_screen_name,
        }


def get_user_agent():
    return choice([
        'Mozilla/4.0 (compatible; Windows NT 5.1; .NET CLR '
        '1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR '
        '3.5.30729)',
        'Mozilla/4.0 (compatible; Windows NT 5.2; SV1; .NET CLR '
        '1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.04506.30)',
        'Mozilla/4.0 (compatible; Windows NT 5.2; Win64; x64; SV1)',
        'Mozilla/4.0 (compatible; Windows NT 5.2; .NET CLR '
        '1.1.4322)',
        'Mozilla/4.0 (compatible; Windows NT 6.0; SLCC1; .NET CLR '
        '2.0.50727; .NET CLR 3.0.04506; .NET CLR 1.1.4322; InfoPath.2; .NET '
        'CLR 3.5.21022)',
        'Mozilla/4.0 (compatible; Windows NT 6.1; Trident/4.0; '
        'SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; '
        'Media Center PC 6.0; .NET CLR 1.1.4322; Tablet PC 2.0; '
        'OfficeLiveConnector.1.3; OfficeLivePatch.1.3; MS-RTC LM 8; '
        'InfoPath.3)',
        'Mozilla/4.0 (compatible; Windows NT 5.1; Trident/4.0; '
        'FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)',
        'Mozilla/5.0 (Windows; U; Win95; it; rv:1.8.1) Gecko/20061010 '
        'Firefox/2.0',
        'Mozilla/5.0 (Windows; U; Windows NT 6.0; zh-HK; rv:1.8.1.7) Gecko '
        'Firefox/2.0',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; pt-BR; rv:1.8.1.15) '
        'Gecko/20080623 Firefox/2.0.0.15',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; es-AR; rv:1.9) '
        'Gecko/2008051206 Firefox/3.0',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_5_6 ; nl; rv:1.9) '
        'Gecko/2008051206 Firefox/3.0',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; es-AR; rv:1.9.0.11) '
        'Gecko/2009060215 Firefox/3.0.11',
        'Mozilla/5.0 (X11; U; Linux x86_64; cy; rv:1.9.1b3) Gecko/20090327 '
        'Fedora/3.1-0.11.beta3.fc11 Firefox/3.1b3',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; ja; rv:1.9.2a1pre) '
        'Gecko/20090403 Firefox/3.6a1pre',
        'Mozilla/4.0 (compatible; 6.0; Mac_PowerPC; en) Opera 9.00',
        'Mozilla/5.0 (X11; Linux i686; U; en) Opera 9.00',
        'Mozilla/4.0 (compatible; Mac_PowerPC; en) Opera 9.00',
        'Opera/9.00 (Nintindo Wii; U; ; 103858; Wii Shop Channel/1.0; en)',
        'Mozilla/4.0 (compatible; Windows NT 6.0; pt-br) Opera 9.25',
        'Opera/9.50 (Macintosh; Intel Mac OS X; U; en)',
        'Opera/9.61 (Windows NT 6.1; U; zh-cn) Presto/2.1.1',
        'Mozilla/5.0 (Windows NT 5.0; U; en-GB; rv:1.8.1) Gecko/20061208 '
        'Firefox/2.0.0 Opera 9.61',
        'Opera/10.00 (X11; Linux i686; U; en) Presto/2.2.0',
        'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en; rv:1.8.1) '
        'Gecko/20061208 Firefox/2.0.0 Opera 10.00',
        'Mozilla/4.0 (compatible; X11; Linux i686 ; en) Opera 10.00',
        'Opera/9.80 (Windows NT 6.0; U; fi) Presto/2.2.0 Version/10.00',
        'Mozilla/5.0 (Macintosh; U; PPC Mac OS X; de-de) AppleWebKit/412.6 '
        '(KHTML, like Gecko) Safari/412.2',
        'Mozilla/5.0 (Windows; U; Windows NT 5.1; id) AppleWebKit/522.11.3 '
        '(KHTML, like Gecko) Version/3.0 Safari/522.11.3',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; da) AppleWebKit/522.15.5 '
        '(KHTML, like Gecko) Version/3.0.3 Safari/522.15.5',
        'Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; ar) '
        'AppleWebKit/525.18 (KHTML, like Gecko) Version/3.1.1 Safari/525.18',
        'Mozilla/5.0 (Mozilla/5.0 (iPhone; U; CPU iPhone OS 2_0_1 like Mac OS '
        'X; hu-hu) AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 '
        'Mobile/5G77 Safari/525.20',
        'Mozilla/5.0 (iPod; U; CPU iPhone OS 2_2_1 like Mac OS X; es-es) '
        'AppleWebKit/525.18.1 (KHTML, like Gecko) Version/3.1.1 Mobile/5H11 '
        'Safari/525.20',
        'Mozilla/5.0 (Windows; U; Windows NT 6.0; he-IL) AppleWebKit/528.16 '
        '(KHTML, like Gecko) Version/4.0 Safari/528.16',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_1; zh-CN) '
        'AppleWebKit/530.19.2 (KHTML, like Gecko) Version/4.0.2 Safari/530.19',
    ])

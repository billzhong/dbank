#!/usr/bin/env python

import argparse
import urllib2
import re
import json
import base64
import hashlib
import distutils.spawn
import subprocess
import os.path


# decrypt 'eb' type, NO test.
def decrypt_c(h, l):
    k = []
    e = 0
    g = ''
    f = 0
    while f < 256:
        k[f] = f

        f += 1
    f = 0
    while f < 256:
        e = (e + k[f] + h[f % len(h)]) % 256
        d = k[f]
        k[f] = k[e]
        k[e] = d

        f += 1
    f = 0
    e = 0
    m = 0
    while m < len(l):
        f = (f + 1) % 256
        e = (e + k[f]) % 256
        d = k[f]
        k[f] = k[e]
        k[e] = d
        g += l[m] ^ k[(k[f] + k[e]) % 256]
        m += 1
    return g


# decrypt 'ed' type, tested.
def decrypt_b(d, e):
    g = ''
    l = len(e)
    f = len(d)
    h = 0
    while h < f:
        k = ord(d[h]) ^ ord(e[h % l])
        k = chr(k)
        g += k
        h += 1
    return g


# decrypt link data, there is two type crypts, only test the 'ed' one.
def decrypt(g, e):
    g = base64.decodestring(g)
    f = e[0:2]

    if f == 'ea':
        d = g
    elif f == 'eb':
        d = decrypt_b(g, decrypt_c(e, e))
    elif f == 'ed':
        d = decrypt_b(g, hashlib.md5(e).hexdigest())
    else:
        d = g

    return d


def is_htmlfile(file_name):
    """ dbank will return html code sometimes. detect it. """
    if os.path.exists(file_name):
        with open(file_name) as f:
            head = f.read(9)
            if head == '<!DOCTYPE':
                return True
    return False


# call wget to download
def wget_download(download_url, file_name='', resume=False):
    wget_cmd = ['wget', download_url]
    if file_name != '':
        wget_cmd.append('-O')
        wget_cmd.append(file_name)
    if resume and not is_htmlfile(file_name):
        wget_cmd.append('-c')
    assert distutils.spawn.find_executable(wget_cmd[0]), "Cannot find %s" % wget_cmd[0]
    exit_code = subprocess.call(wget_cmd)
    if exit_code != 0:
        raise Exception('Cannot call wget to download.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='DBank Downloader')
    parser.add_argument('url', help='DBank URL')
    parser.add_argument('--resume', help='Resume getting a partially-downloaded file.', action='store_true')
    parser.add_argument('--only-showurl', dest='showurl', help='No download, only show download url', action='store_true')
    args = parser.parse_args()

    # replace dbank.com to vmail.com in url
    args.url = args.url.replace('dbank.com', 'vmall.com')

    # check the url contain vmail.com
    if args.url.find('vmall.com') == -1:
        raise Exception('URL must contain dbank.com or vmall.com.')

    # use urllib2 to get html data
    try:
        request = urllib2.Request(args.url)
        request.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_2) \
                            AppleWebKit/536.26.17 (KHTML, like Gecko) Version/6.0.2 Safari/536.26.17')
        html = urllib2.urlopen(request).read()
    except:
        raise Exception('Please check the URL.')

    # check the html data contain <head> keyword
    if html.find('<head>') == -1:
        raise Exception('Cannot get correct html page.')

    # use regexp to search the link data
    try:
        m = re.search('globallinkdata = {(.*?)};', html)
        data = '{' + m.group(1) + '}'
        result = json.loads(data)
    except:
        raise Exception('Cannot get the link data.')

    # process the link data to get key
    e = result['data']['encryKey']

    # download all files
    for files in result['data']['resource']['files']:
        fn = files['name']
        downloadurl = files['downloadurl']
        url = decrypt(downloadurl, e)

        if args.showurl:
            print('%s: %s' % (fn, url))
        elif args.resume:
            wget_download(url, fn, True)
        else:
            wget_download(url, fn)

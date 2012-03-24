#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Only:
1. useful @ celebritymoviearchive.com
2. Tested on OSX Lion 7.3 with python 2.7, never tested on other platforms, requires Beautiful Soup 4 (at least the beta version)

To-do:
    1. CMA randomly forbid the automatic way to download their images(url redirect to their banner image), gotta be a way to fix it.
    2. ...
'''

from bs4 import BeautifulSoup
from urlgrabber.progress import text_progress_meter
import re
import os
import sys
import getopt
import urllib
import urllib2
import urlgrabber
import logging

reload(sys)
sys.setdefaultencoding('utf-8')
logging.basicConfig(format = '%(asctime)s %(message)s', filename='output.log',level=logging.DEBUG)
USAGE = '''
Usage: cma_downloader.py [arguments] 

Arguments:
    -h          display this help and exit
    -c          cma celeb's page url: ***name.php***
    -p          single cma's url: ***movie.php***

Examples:
    Bet you already know it...
'''

def page_download(page_url):
    page = urllib2.urlopen(page_url)
    soup = BeautifulSoup(page, 'html5lib')
    pattern = re.findall(r'Celebrity Movie Archive :: (.*)', soup.title.string, re.M)
    temp = {}
    title = str(pattern[0]).split()
    image_list = soup.find_all('img')
    for image in image_list:
        image_str_list = str(image).split()
        for n in xrange(len(image_str_list)):
            if image_str_list[n] in title:
                temp[title.index(image_str_list[n])] = image_str_list[n]
        if len(temp) >= 2:
            src_url = re.findall(r'src=\"(.*)\"/>', str(image), re.M)
            tgt_url = str(urllib.unquote(src_url[0].encode('ascii')).decode('utf-8'))
            tgt_name = str(os.path.basename(tgt_url))
            print 'saving : ' + tgt_url + ' to ' + tgt_name
            try:
                urlgrabber.urlgrab(tgt_url, tgt_name, progress_obj=urlgrabber.progress.TextMeter())
            except Exception, e: 
                print 'Oops: ' + str(e)
                logging.exception('Problem occurs when grabbing: ' + tgt_url)

def celeb_parse(celeb_url):
    page = urllib2.urlopen(celeb_url)
    soup = BeautifulSoup(page, 'html5lib')
    dup_list = soup.find_all(href = re.compile('movie.php'))
    link_list = []
    for url in dup_list:
        if 'eye.gif' in str(url):
            link_list.append('http://www.celebritymoviearchive.com' + (re.findall(r'a href=\"(.*)\">', str(url), re.M))[0])
    for link in link_list:
        print 'Downloading single album: ' + link
        page_download(link)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'p:hc:', ['page=', 'celebrity='])
    except getopt.GetoptError, err:
        # print help information and exit:
        print USAGE
        sys.exit(2)
    for o, v in opts:
        if o == '-p':
            print 'downloading images @ ' + v
            page_download(v)
        elif o == '-c':
            print 'download celeb\'s all images @ ' + v
            album_list = celeb_parse(v)
            sys.exit()
        elif o in ('-h', '--help'):
            print USAGE
            sys.exit()
        else:
            assert False, 'unhandled option'

if __name__ == '__main__':
    main()

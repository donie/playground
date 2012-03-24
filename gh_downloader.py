#!/usr/bin/env python
#-*- coding: utf-8 -*-
'''
Only:
1. useful @ HC, hope they didn't change their html too often...
2. Tested on OSX Lion 7.3 with python 2.7, never tested on other platforms, requires Beautiful
Soup 4 (at least the beta version)

To-do:
    1. use PY libs to do the download...
    2. Exception handler 
'''

from bs4 import BeautifulSoup
from urlgrabber.progress import text_progress_meter
import re
import os
import sys
import getopt
import urllib2
import urlgrabber
import logging

reload(sys)
sys.setdefaultencoding('utf-8')
logging.basicConfig(format = '%(asctime)s %(message)s', filename='output.log',level=logging.DEBUG)
sfx = ('small.jpg', 'small.gif', 'small.png')
USAGE = '''
Usage: gh_downloader.py [arguments] 

Arguments:
    -h          display this help and exit
    -u          hc user's id
    -p          hc album's first page, please note, better be with the first page of the album

Examples:
    gh_downloader.py  -p http://my.hoopchina.com/3158969/photo/a39816-2.html
    gh_downloader.py  -u 3158969
    gh_downloader.py  -h
'''

def if_next(page_url):
    page = urllib2.urlopen(page_url)
    soup = BeautifulSoup(page)
    if len(soup.find_all("a", { "class" : "next" })) == 1:
        return "http://my.hoopchina.com" + soup.find_all("a", { "class" : "next" })[0].get('href')
    else: 
        print "----------------------------------"
        print "no more pages"
        print "----------------------------------"

def user_album(album_url):
    albums = urllib2.urlopen(album_url)
    soup = BeautifulSoup(albums, from_encoding="gb18030").find_all("div", { "class" : "album_list" })
    result = re.findall(r'<a href="(.*)"><img', str(soup), re.M)
    album_list = {}
    for a in result:
        alt = re.findall('<a href="' + str(a) + "\"><img alt=\"(.*)\" border", str(soup), re.M)
        print "creating directory: " + str(alt[0])
        os.system("mkdir \"" + str(alt[0]) + "\"")
        album_list[str(alt[0])] = "http://my.hoopchina.com" + a
        continue
    return album_list

def user_album_download(album_list):
    for folder, album in album_list.iteritems():
        print "downloading images @ " + album
        page_download(album, folder)
        while not if_next(album) is None:
            v = if_next (album)
            page_no = page_no + 1
            print "----------------------------------"
            print "Page"+ str(page_no) + ":url is " + album
            print "----------------------------------"
            page_download(album, folder)
            continue

def page_download(page_url, folder):
    page = urllib2.urlopen(page_url)
    soup = BeautifulSoup(page)
    print len(soup.find_all("a", { "class" : "next" }))
    for src in soup.find_all('img'):
        if src.get('src').endswith(sfx):
            tgt_url = str(src.get('src').replace('small', 'big'))
            print "saving : " + tgt_url 
            tgt_name = os.path.basename(tgt_url)
            try:
                urlgrabber.urlgrab(tgt_url, "./" + folder + "/" + tgt_name, progress_obj=urlgrabber.progress.TextMeter())
            except Exception, e: 
                print "Oops: " + str(e)
                logging.exception("Problem occurs when grabbing: " + tgt_url)
                
def main():
    print "Started"
    try:
        opts, args = getopt.getopt(sys.argv[1:], "p:hu:", ["page=", "user="])
    except getopt.GetoptError, err:
        # print help information and exit:
        print USAGE
        sys.exit(2)
    page_no = 1 
    user = False
    for o, v in opts:
        if o == "-p":
            print "downloading images @ " + v
            page_download(v, '')
            while not if_next(v) is None:
                v = if_next (v)
                page_no = page_no + 1
                print "----------------------------------"
                print "Page"+ str(page_no) + ":url is " + v
                print "----------------------------------"
                page_download(v, '')
                continue
        elif o == "-u":
            v = "http://my.hoopchina.com/" + v + "/photo"
            print "download user's all albums @ " + v
            album_list = user_album(v)
            user_album_download(album_list)
            while not if_next(v) is None:
                v = if_next (v)
                page_no = page_no + 1
                print "----------------------------------"
                print "User's page "+ str(page_no) + "'s url is " + v
                print "----------------------------------"
                album_list = user_album(v)
                user_album_download(album_list)
                continue
            sys.exit()
        elif o in ("-h", "--help"):
            print USAGE
            sys.exit()
        else:
            assert False, "unhandled option"

if __name__ == '__main__':
    main()

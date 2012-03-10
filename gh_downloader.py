#!/usr/bin/env python

from bs4 import BeautifulSoup
import re
import os
import sys
import getopt
import urllib2

sfx = ('small.jpg', 'small.gif', 'small.png')
USAGE = '''
Usage: gh_downloader.py [arguments] 

Arguments:
    -h          display this help and exit
    -u          hc user's id
    -p          hc album's first page, please note, better be with the first page of the album

Examples:
    gh_downloader.py  -p
    gh_mkfakefile.py  -h 
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

def page_download(page_url):
    page = urllib2.urlopen(page_url)
    soup = BeautifulSoup(page)
    print len(soup.find_all("a", { "class" : "next" }))
    for src in soup.find_all('img'):
        if src.get('src').endswith(sfx):
            #tgt_url = src.get('src').replace('small', '')
            print src.get('src').replace('small', 'big')

def main():
    print "Started"
    url = "http://my.hoopchina.com/lishg1990/photo/a70625-1.html"
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
            page_download(v)
            while not if_next(v) is None:
                v = if_next (v)
                page_no = page_no + 1
                print "----------------------------------"
                print "Page"+ str(page_no) + ":url is " + url
                print "----------------------------------"
                page_download(v)
                continue
        elif o == "-u":
            print "lol @ " + v
            sys.exit()
        elif o in ("-h", "--help"):
            print USAGE
            sys.exit()
        else:
            assert False, "unhandled option"

if __name__ == '__main__':
  main()

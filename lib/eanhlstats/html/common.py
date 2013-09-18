'''Common functions for html parsing'''
# -*- coding: utf-8 -*-
import urllib2

PARTIAL_URL_PREFIX = "http://www.easportsworld.com/en_US/clubs/partial/NHL14"


def get_content(url):
    '''Get html content of given url.
    untested copy/paste code'''
    content = None
    if url:
        try:
            url_handle = urllib2.urlopen(url, timeout=60)
            content = url_handle.read()
            url_handle.close()
        except IOError, error:
            print 'We failed to open "%s".' % url
            if hasattr(error, 'code'):
                print 'We failed with error code - %s.' % error.code
            elif hasattr(error, 'reason'):
                print "The error object has the following 'reason' attribute :"
                print error.reason
                print "This usually means the server doesn't exist,",
                print "is down, or we don't have an internet connection."
    return content

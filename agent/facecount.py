#!/usr/bin/env python

# SenSafety.MidTerm.agent.facecount runs as an agent on a remote system and
# detects new xml files containing face detection information. The information
# is converted into facecount events and posted to the CEPengine using http.

# Marc de Lignie, Politie IV-organisatie
# September 10, 2014

import os, sys, uuid, time, urllib, urllib2, socket

INTERVAL = 1                # Poll the file system about every INTERVAL seconds
FACECOUNT = 'Facecount'     # Name of the event stream in the CEPengine


class FaceCount(object):

    def __init__(self, xmldir, url, interval):
        self._xmldir = xmldir
        self._url = url + '?stream=' + FACECOUNT + '&'
        self._interval = interval
        self._dircache = set([])   # Access each xml file only once
        macstr = ('%012X' % uuid.getnode()).upper()
        self._mac = '%2s:%2s:%2s:%2s:%2s:%2s' % tuple(
                    [macstr[x:x+2] for x in xrange(0, 12, 2)])
        self._connected = True
        socket.setdefaulttimeout(1)
          
    def run(self):
        lasttime = time.time()
        while True:
            thistime, xmlstr = self._getXML(lasttime)
            if thistime > lasttime:
                self._postData(self._getEvent(thistime, xmlstr))
                lasttime = thistime
            time.sleep(self._interval)

    def _getXML(self, lasttime):
        xmlstr = None
        thistime = lasttime
        dirlist = set(os.listdir(self._xmldir))
        for filename in dirlist - self._dircache:
            pathname = os.path.join(self._xmldir, filename)
            thistime = os.lstat(pathname).st_ctime
            if thistime > lasttime: # creation time
                if xmlstr:
                    raise RuntimeWarning(''.join([
                        'XML file creation interval ',
                        'is smaller than the poll interval']))
                else:
                    xmlstr = ''.join(open(pathname).readlines())
        self._dircache = dirlist
        return thistime, xmlstr

    def _getEvent(self, thistime, xmlstr):
        # Simple xml structure can be parsed with the standard library
        nframe = xmlstr.count('<frame ')
        nid = xmlstr.count('person id=')
        return {
            'timestamp': time.strftime("%Y-%m-%dT%H:%M:%S",   # ISO 8601
                                       time.localtime(thistime)),
            'cam': self._mac,
            'facecount': float(nid) / nframe
            }

    def _postData(self, eventdict):
        print eventdict
        try:
            eventurl = self._url + urllib.urlencode(eventdict)
            urllib2.urlopen(eventurl)
            if not self._connected:
                print "Connection available"
                self._connected = True
        except urllib2.URLError:
            if self._connected:
                print "Connection not available"
                self._connected = False
                

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: python facecount.py /home/path/to/xmlfiles \
                      http://www.example.com:3433/sensafety"
    fc = FaceCount(sys.argv[1], sys.argv[2], INTERVAL)
    fc.run()
    


#!/usr/bin/env jython

# SenSafety.MidTerm.CEPengine provides the Esper based complex event processing
# engine for the mid-term SenSafety demo. 
# The module ilpcontrol interfaces with the Intelligent Lamp Posts and provides
# usage scenarios for silent and tilt events.

# The ILP http API has the following functions:
# http://<ip-address>/rpc/ilp/run?busy%20x with 1 <= x<= 4
# http://<ip-address>/rpc/ilp/run?tilt%20x with x = 0 white
#                                               x = 1 red
#                                               x = 2 green
#                                               x = 3 blue
#                                               x = 4 white
#                                               x = 5 yellow
#                                               x = 6 yellow
# http://<ip-address>/rpc/ilp/run?silence%20x with x = 0, 1 direction
# http://<ip-address>/rpc/ilp/run?dim%20x with x percentage 0-100
# http://<ip-address>/rpc/ilp/run?color%20x with x as for tilt

# Marc de Lignie, Politie IV-organisatie, COMMIT/
# Okt 07, 2014

import threading, time, urllib, urllib2

ILPTOPICS = ['ilp1', 'ilp2/']  # A topic for each ILP
ILPURLS = ['http://145.136.28.75:80/rpc/ilp/run',
           'http://145.136.28.64:80/rpc/ilp/run']


class ILPControl(object):

    def __init__(self, pahoclient, maxbusy, minquiet, initintens=50, 
                       initcolor=0x33AA44, initdirect=50):
        self._pahoclient = pahoclient
        self._locked = False
        self.setILPS(initintens, initcolor, initdirect)
        self._MAXBUSY = maxbusy
        self._MINQUIET = minquiet
        self._nquiet = 0
        self._busylevel = 0
            
    def setILPS(self, intens, color, direct):
        print "Initial settings ILPS"
        self._intens = intens
        self._color = color
        self._direct = direct
        self._postEvent(intens, color, direct)
        return True
        
    def getILPS(self):
        return self._intens, self._color, self._direct
        
    def _postEvent(self, intens, color, direct):
        for topic in ILPTOPICS:
            tinit = time.time()
            timestamp = time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time.time()))
            self._pahoclient.publish(topic, 0, 
                ''.join(['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
                '<Payload driver_version="1" request_id="220">',
                '<Parameter name="timestamp">%s</Parameter>' % timestamp,
                '<Parameter name="direction">%i</Parameter>' % direct,
                '<Parameter name="intensity">%i</Parameter>' % intens,
                '<Parameter name="color">%0X</Parameter>' % color,
                '</Payload>']))
#            print "Mqtt message sent on topic " + topic + \
#                  "(%i, %0.6X, %i)"%(intens, color, direct) + ": %f" % (time.time()-tinit)
            
    def tilt(self):
        # Flash orange 0.1s High, 0.2s Low, three times
        # Threaded for non-blocking calls
        if self._locked:
            print "ILPs locked; Tilt event ignored"
            return False
        self._locked = True
        t = threading.Thread(target=self._innerTilt)
        t.start()
        return True
        
    def _innerTilt(self):
        print "Tilt scenario played on ILPs"
        t1 = threading.Thread(target=self._postILP1tilt)
        t1.start()
        t2 = threading.Thread(target=self._postILP2tilt)
        t2.start()
#        for url in ILPURLS:    urllib2 times out which is annoying
#            urltilt = url + '?tilt%201'
#            try:
#                urllib2.urlopen(urltilt)
#            except:
#                self._locked = False
#                print 'Cannot reach ' + urltilt 
        timehigh = 0.2
        timelow = 0.1
        N = 3
        COLOR = 0xFF9900  # Should be orange
        DIRECT = 50
        for i in xrange(N):
            self._postEvent(255, COLOR, DIRECT)
            time.sleep(timehigh)
            self._postEvent(10, COLOR, DIRECT)
            time.sleep(timelow)
        self._postEvent(self._intens, self._color, self._direct)
        self._locked = False
        
    def _postILP1tilt(self):
        urltilt = ILPURLS[0] + '?tilt%201'
        try:
            urllib2.urlopen(urltilt)
        except:
            print 'Cannot reach ' + urltilt 
                
    def _postILP2tilt(self):
        urltilt = ILPURLS[1] + '?tilt%201'
        try:
            urllib2.urlopen(urltilt)
        except:
            print 'Cannot reach ' + urltilt 
                
    def silent(self):
        # Move blue 0.5s moving, 0.5s static, 10 times
        # Threaded for non-blocking calls
        self._locked = True
        t = threading.Thread(target=self._innerSilent)
        t.start()
        return True
        
    def _innerSilent(self):
        print "Silence scenario played on ILPs"
        t1 = threading.Thread(target=self._postILP1silence)
        t1.start()
        t2 = threading.Thread(target=self._postILP2silence)
        t2.start()
        time.sleep(2)
        t3 = threading.Thread(target=self._postILP1silence)
        t3.start()
        t4 = threading.Thread(target=self._postILP2silence)
        t4.start()
#        for url in ILPURLS:   #urllib2 times out
#            urlsilence = url + '?tilt%203'
#            try:
#                urllib2.urlopen(urlsilence)
#            except:
#                self._locked = False
#                print 'Cannot reach ' + urlsilence 
        timemoving = 0.5
        timestatic = 0.5
        N = 2
        NSTEP = 50
        INTENS = 255
        DIRECT = 255
        COLOR = 0x0000FF  # Should be blue
        for i in xrange(N):
            for j in xrange(0, DIRECT, NSTEP):
                self._postEvent(INTENS, COLOR, j)
                time.sleep(timemoving/NSTEP)
            time.sleep(timestatic)
        self._postEvent(self._intens, self._color, self._direct)
        self._locked = False

    def _postILP1silence(self):
        urlsilence = ILPURLS[0] + '?tilt%203'
        try:
            urllib2.urlopen(urlsilence)
        except:
            print 'Cannot reach ' + urlsilence
                
    def _postILP2silence(self):
        urlsilence = ILPURLS[1] + '?tilt%203'
        try:
            urllib2.urlopen(urlsilence)
        except:
            print 'Cannot reach ' + urlsilence
                
    def busy(self, busy):
        # Adjust busy level
        if busy:
            self._busylevel += 1
        else:
            self._busylevel -= 1
        print "Busy level: ", self._busylevel
        if self._busylevel > self._MAXBUSY: # Already on maximum
            self._busylevel -= 1 
            return
        elif self._busylevel >= 0:
            self._busySetILPS(self._busylevel)
        elif self._busylevel == self._MINQUIET:
            if self._locked:
                print "ILPs locked; Silent event postponed"
                return False
            else:
                self.silent()
                self._busylevel = 0
        return True  


    def _busySetILPS(self, busylevel):
        if self._locked:
            print "ILPs locked; Busy event ignored"
            return
        print "Busy level set on ILPs"
        t1 = threading.Thread(target=self._postILP1busy)
        t1.start()
        t2 = threading.Thread(target=self._postILP2busy)
        t2.start()
#        for url in ILPURLS:
#            level = busylevel
#            if level > 4:
#                level = 4
#            if level < 1:
#                level = 1            
#            urlbusy = url + '?busy%20' + str(level)
#            try:
#                urllib2.urlopen(urlbusy)
#            except:
#                print 'Cannot reach ' + urlbusy
        LEVELSTEP = 20
        rgbcolor = []
        rgbcolor.append(self._color/(256**2))
        rgbcolor.append((self._color - rgbcolor[0]*256**2)/256)
        rgbcolor.append(self._color - rgbcolor[0]*256**2 - rgbcolor[1]*256)
        rgbcolor[0] = min(255, rgbcolor[0] + busylevel * LEVELSTEP)
        rgbcolor[1] = max(0, rgbcolor[1] - busylevel * LEVELSTEP)
        rgbcolor[2] = max(0, rgbcolor[2] - busylevel * LEVELSTEP)
        hexcolor = rgbcolor[0]*256**2 + rgbcolor[1]*256 + rgbcolor[2]
        self._postEvent(self._intens, hexcolor, self._direct)

    def _postILP1busy(self):
        level = 1
        if self._busylevel == self._MAXBUSY:
            level = 4
        urlbusy = ILPURLS[0] + '?busy%20' + '%i'%(level)
        try:
            urllib2.urlopen(urlbusy)
        except:
            print 'Cannot reach ' + urlbusy 
                
    def _postILP2busy(self):
        level = 1
        if self._busylevel == self._MAXBUSY:
            level = 4
        urlbusy = ILPURLS[1] + '?busy%20' + '%i'%(level)
        try:
            urllib2.urlopen(urlbusy)
        except:
            print 'Cannot reach ' + urlbusy 
                


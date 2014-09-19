#!/usr/bin/env jython

# SenSafety.MidTerm.CEPengine provides the Esper based complex event processing
# engine for the mid-term SenSafety demo. 
# The module ilpcontrol interfaces with the Intelligent Lamp Posts and provides
# usage scenarios for silent and tilt events.

# Marc de Lignie, Politie IV-organisatie, COMMIT/
# Sept 18, 2014

import threading, time
ILPTOPICS = ['ilp1', 'ilp2']  # A topic for each ILP


class ILPControl(object):

    def __init__(self, pahoclient, initintens=50, 
                 initcolor=0x33AA44, initdirect=50):
        self._pahoclient = pahoclient
        self._locked = False
        self._busylevel = 0
        self._busyTimeout()
        self.setILPS(initintens, initcolor, initdirect)
            
    def setILPS(self, intens, color, direct):
        if self._locked:
            return False
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
            self._pahoclient.publish(topic, 1, 
                ''.join(['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
                '<Payload driver_version="1" request_id="220">',
                '<Parameter name="timestamp">2014-03-28T07:11:33+00:00</Parameter>',
                '<Parameter name="direction">%i</Parameter>' % direct,
                '<Parameter name="intensity">%i</Parameter>' % intens,
                '<Parameter name="color">%X</Parameter>' % color,
                '</Payload>']))
            print "Mqtt message sent on topic " + topic + \
                  str((intens, color, direct)) + ": %f" % (time.time()-tinit)
            
    def tilt(self):
        # Flash orange 0.1s High, 0.2s Low, three times
        # Threaded for non-blocking calls
        if self._locked:
            return False
        self._locked = True
        t = threading.Thread(target=self._innerTilt)
        t.start()
        return True
        
    def _innerTilt(self):
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
                
    def silent(self):
        # Move blue 0.5s moving, 0.5s static, 10 times
        # Threaded for non-blocking calls
        if self._locked:
            return False
        self._locked = True
        t = threading.Thread(target=self._innerSilent)
        t.start()
        return True
        
    def _innerSilent(self):
        timemoving = 0.5
        timestatic = 0.5
        N = 10
        NSTEP = 10
        INTENS = 255
        DIRECT = 255
        COLOR = 0x0000FF  # Should be blue
        for i in xrange(N):
            for j in xrange(0, DIRECT, NSTEP):
                self._postEvent(INTENS, COLOR, j)
                time.sleep(timemoving/NSTEP)
            self._postEvent(INTENS, COLOR, self._direct)
            time.sleep(timestatic)
        self._postEvent(self._intens, self._color, self._direct)
        self._locked = False

    def busy(self):
        # Increase busy level used by self._busyTimeout
        MAXLEVEL = 3
        if self._busylevel < MAXLEVEL:
            self._busylevel += 1
            self._busySetILPS()

    def _busyTimeout(self):
        # Decrease busy level automatically every TTIMEOUT seconds
        MINLEVEL = 0
        TTIMEOUT = 60.
        if self._busylevel > MINLEVEL:
            self._busylevel -= 1
            self._busySetILPS()
        threading.Timer(TTIMEOUT, self._busyTimeout)

    def _busySetILPS(self):
        if self._locked:
            return
        LEVELSTEP = 20
        rgbcolor = tuple(int(self._color[i:i+2], 16) for i in range(2, 8, 2))
        rgbcolor[0] = min(255, rgbcolor[0] + self._busylevel * LEVELSTEP)
        rgbcolor[1] = max(0, rgbcolor[1] - self._busylevel * LEVELSTEP)
        rgbcolor[2] = max(0, rgbcolor[2] - self._busylevel * LEVELSTEP)
        hexcolor = '%02X%02X%02X' % rgbcolor
        self._postEvent(self._intens, hexcolor, self._direct)


#!/usr/bin/env jython

# SenSafety.MidTerm.CEPengine provides the Esper based complex event processing
# engine for the mid-term SenSafety demo. 
# The module eventgenerator provides a few types of random events for testing

# Marc de Lignie, Politie IV-organisatie, COMMIT/
# May 8, 2014

import random, time, urllib, urllib2, threading
from main import ANOMALOUS_SOUND
from mqttsensors import TILTTOPIC

ILPTOPIC = 'ilp'

class AnomalousSound(threading.Thread):
    def __init__(self, url, interval):
        threading.Thread.__init__(self)
        self._url = url + '?stream=' + ANOMALOUS_SOUND + '&'
        self._interval = interval
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()
    
    def run(self):
        print 'Http anomalous sound message generator started'
        while not self._stop.isSet():
            self.postEvent()
            time.sleep(2. * self._interval * random.random())
            
    def postEvent(self):
        print 'Anomalous sound event posted'
        eventdata = {
            'timestamp': '2014-04-10T11:22:33.44+02:00', # ISO 8601
            'geoNB': '52.12345',                         # ISO 6709
            'geoEL': '5.12345',
            'MAC': '01-23-45-67-89-ab',
            'probability': 33 }
        # Posts on the http interface to be used by Viet Duc's Sound app
        # urlencode converts ':' into '%3A'
        # Events can also be posted manually using an ordinary browser
        eventurl = self._url + urllib.urlencode(eventdata)
        urllib2.urlopen(eventurl)

     
class Tilt(threading.Thread):

    def __init__(self, pahoclient, interval):
        threading.Thread.__init__(self)
        self._pahoclient = pahoclient
        self._interval = interval
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()
    
    def run(self):
        print 'Mqtt tilt message generator started'
        while not self._stop.isSet():
            self.postEvent()
            time.sleep(2. * self._interval * random.random())

    def postEvent(self):
        self._pahoclient.publish(TILTTOPIC, 1, 
            ''.join(['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Payload driver_version="1" request_id="220">',
            '<Parameter name="timestamp">2014-03-28T07:11:33+00:00</Parameter>',
            '<Parameter name="previous_timestamp">',
                '2014-03-28T07:11:32+00:00</Parameter>',
            '<Parameter name="event">MOTIONSTART</Parameter>',
            '<Parameter name="state">MOTION</Parameter>',
            '</Payload>']))
        print 'Mqtt message sent on topic ' + TILTTOPIC


class ILP_control(threading.Thread):

    def __init__(self, pahoclient, interval):
        threading.Thread.__init__(self)
        self._pahoclient = pahoclient
        self._interval = interval
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()
    
    def run(self):
        print 'Mqtt ILP_control message generator started'
        while not self._stop.isSet():
            self.postEvent()
            time.sleep(2. * self._interval * random.random())

    def postEvent(self):
        self._pahoclient.publish(ILPTOPIC, 1, 
            ''.join(['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Payload driver_version="1" request_id="220">',
            '<Parameter name="timestamp">2014-03-28T07:11:33+00:00</Parameter>',
            '<Parameter name="direction">50</Parameter>',
            '<Parameter name="intensity">50</Parameter>',
            '<Parameter name="color">0x33AA44</Parameter>',
            '</Payload>']))
        print 'Mqtt message sent on topic ' + ILPTOPIC




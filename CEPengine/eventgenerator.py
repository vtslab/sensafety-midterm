#!/usr/bin/env jython

# SenSafety.MidTerm.CEPengine provides the Esper based complex event processing
# engine for the mid-term SenSafety demo. 
# The module eventgenerator provides a few types of random events for testing

# Marc de Lignie, Politie IV-organisatie, COMMIT/
# April 10, 2014

import threading, random, time, urllib, urllib2
from main import ANOMALOUS_SOUND


class AnomalousSound(threading.Thread):

    def __init__(self, url, interval):
        self._url = url + '?stream=' + ANOMALOUS_SOUND + '&'
        self._interval = interval
    
    def start(self):
        while True:
            self.postEvent()
            time.sleep(2. * self._interval * random.random())
            
    def postEvent(self):
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

    def __init__(self, mqttbroker, port, interval):
        self._broker = mqttbroker
        self._port = port
        self._interval = interval
    
    def start(self):
        while True:
            self.postEvent()
            time.sleep(2. * self._interval * random.random())

    def postEvent(self):
        pass


#!/usr/bin/env jython

# SenSafety.MidTerm.CEPengine provides the Esper based complex event processing
# engine for the mid-term SenSafety demo. 
# The module eventgenerator provides a few types of random events for testing

# Marc de Lignie, Politie IV-organisatie, COMMIT/
# Sept 25, 2014

import random, time, urllib, urllib2, threading
import simplejson as json
import nl.noldus.nmf.NCNmfProducer as NCNmfProducer
import nl.noldus.nmf.NCNmfTypes as NCNmfTypes
from mqttsensors import TILTTOPIC
from httpsensors import FACECOUNT


class AnomalousSound(threading.Thread):
    def __init__(self, interval, exchange):
        threading.Thread.__init__(self)
        self._interval = interval
        self._stop = threading.Event()
        self.producer = NCNmfProducer()
        self.producer.Open("127.0.0.1", 5672, "guest", "guest", "")
        self.producer.Bind(
            NCNmfTypes.EExchangeType.eExchangeTypeFanout, exchange)

    def stop(self):
        self._stop.set()
    
    def run(self):
        print 'AMQP anomalous sound message generator started'
        while not self._stop.isSet():
            self.postEvent()
            time.sleep(2. * self._interval * random.random())
            
    def postEvent(self):
        ids = ["00:11:22:33:44:AF", "44:55:66:77:88:BE"]
        eventdata = {
            "message":       "Sweet sound event",
            "id":            ids[random.randrange(len(ids))],
            "soundLevel":    "0.123" }
        # Posts to the local RabbitMQ server using Noldus NCF
        self.producer.Publish(json.dumps(eventdata), "");
        print 'Anomalous sound event posted'

     
class Facecount(threading.Thread):
    """
    Facecount will poll facecount events from a web server.
    The current implementation only acts as event generator.
    """

    def __init__(self, url, interval):
        threading.Thread.__init__(self)
        self._url = url + '?stream=' + FACECOUNT + '&'
        self._interval = interval
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()
    
    def run(self):
        print 'Facecount message generator started'
        while not self._stop.isSet():
            self.postEvent()
            time.sleep(2. * self._interval * random.random())
            
    def postEvent(self):
        # Can be converted into a polling engine of the facecount database
        print 'Facecount event generated'
        eventdict = {
            'timestamp': '2014-04-10T11:22:33.44', # ISO 8601
            'cam': '00:11:22:33:44:FF',
            'facecount': 8.341 }
        eventurl = self._url + urllib.urlencode(eventdict)
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
        self._pahoclient.publish('x/x/Motion/Tilt/MotionStatus/ALERT/00:D0:AA:77:41:6C', 1, 
            ''.join(['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Payload driver_version="1" request_id="220">',
            '<Parameter name="timestamp">2014-03-28T07:11:33</Parameter>',
            '<Parameter name="previous_timestamp">',
                '2014-03-28T07:11:32+00:00</Parameter>',
            '<Parameter name="event">MOTIONSTART</Parameter>',
            '<Parameter name="state">MOTION</Parameter>',
            '</Payload>']))
        print 'Mqtt message sent on topic ' + TILTTOPIC


class Busy(threading.Thread):
    # Busy events will be derived events but are sent directly
    # to the WebMonitor for now
    
    def __init__(self, url, interval):
        threading.Thread.__init__(self)
        self._url = url
        self._interval = interval
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()
    
    def run(self):
        print 'Busy event message generator started'
        while not self._stop.isSet():
            self.postEvent()
            time.sleep(2. * self._interval * random.random())

    def postEvent(self):
        eventdata = {
            'timestamp': '2014-04-10T11:22:33.44', # ISO 8601
            'location': 'Trouw',
            'facecount': 10,
            'soundlevel': 6. }
        urllib2.urlopen(self._url, urllib.urlencode(eventdata))
        print 'Busy event sent to WebMonitor'


class ILP(threading.Thread):

    def __init__(self, pahoclient, interval, ilpclient):
        threading.Thread.__init__(self)
        self._pahoclient = pahoclient
        self._interval = interval
        self._ilpclient = ilpclient
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()
    
    def run(self):
        print 'Mqtt ILP control message generator started'
        time.sleep(5)
        self._ilpclient.tilt()
        time.sleep(5)
        self._ilpclient.silent()
        while not self._stop.isSet():
            self._ilpclient.setILPS(20, 0xAA3344, 20)
            time.sleep(2. * self._interval * random.random())



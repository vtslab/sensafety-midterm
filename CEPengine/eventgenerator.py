#!/usr/bin/env jython

# SenSafety.MidTerm.CEPengine provides the Esper based complex event processing
# engine for the mid-term SenSafety demo. 
# The module eventgenerator provides a few types of random events for testing

# Marc de Lignie, Politie IV-organisatie, COMMIT/
# Sept 10, 2014

import random, time, urllib, urllib2, threading
import simplejson as json
import nl.noldus.nmf.NCNmfProducer as NCNmfProducer
import nl.noldus.nmf.NCNmfTypes as NCNmfTypes
from mqttsensors import TILTTOPIC
from httpsensors import FACECOUNT

ILPTOPIC = 'ilp'

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
        eventdata = {
            "message":       "Sweet sound event",
            "id":            "00:11:22:33:44:AF",
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
            'timestamp': '2014-04-10T11:22:33.44+02:00', # ISO 8601
            'mac': '00:11:22:33:44:FF',
            'facecount': 8 }
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
        self._pahoclient.publish('x/x/Motion/Tilt/MotionStatus/ALERT/x', 1, 
            ''.join(['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',
            '<Payload driver_version="1" request_id="220">',
            '<Parameter name="timestamp">2014-03-28T07:11:33+00:00</Parameter>',
            '<Parameter name="previous_timestamp">',
                '2014-03-28T07:11:32+00:00</Parameter>',
            '<Parameter name="event">MOTIONSTART</Parameter>',
            '<Parameter name="state">MOTION</Parameter>',
            '</Payload>']))
        print 'Mqtt message sent on topic ' + TILTTOPIC


class Silent(threading.Thread):
    # Silent events will be derived events but are sent directly
    # to the WebMonitor for now
    
    def __init__(self, url, interval):
        threading.Thread.__init__(self)
        self._url = url
        self._interval = interval
        self._stop = threading.Event()

    def stop(self):
        self._stop.set()
    
    def run(self):
        print 'Silent event message generator started'
        while not self._stop.isSet():
            self.postEvent()
            time.sleep(2. * self._interval * random.random())

    def postEvent(self):
        eventdata = {
            'timestamp': '2014-04-10T11:22:33.44+02:00', # ISO 8601
            'location': 'Trouw Amsterdam',
            'facecount': 1,
            'soundlevel': 5. }
        urllib2.urlopen(self._url, urllib.urlencode(eventdata))
        print 'Silent event sent to WebMonitor'


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
            'timestamp': '2014-04-10T11:22:33.44+02:00', # ISO 8601
            'location': 'Trouw Amsterdam',
            'facecount': 10,
            'soundlevel': 6. }
        urllib2.urlopen(self._url, urllib.urlencode(eventdata))
        print 'Busy event sent to WebMonitor'


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




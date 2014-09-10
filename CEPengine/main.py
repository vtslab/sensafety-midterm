#!/usr/bin/env jython

"""
SenSafety.MidTerm.CEPengine provides the Esper based complex event processing
engine for the mid-term SenSafety demo. It:
 - activates the Esper CEP engine and registers recognized event types
   (module CEPengine.py)
 - provides an http input channel to sensors that post events of a recognized 
   type (module httpsensors.py)
 - searches the local network for mqtt brokers and subscribes to events
   of a recognized type (mqttsensors.py)
 - registers queries for higher-level events (module queries.py)
 - posts all incoming and inferred events to the situation awareness portal
   (module CEPengine.py)

It should be run with the CEPengine.sh shell script, which defines
the jython classpath and sets the virtualenv environment

CEPengine assumes the presence of sensors that publish sensing events in a 
particular way and in a particular format. The following events are foreseen:
 - fence breach events; published to an mqtt broker in a known format
 - fence tilt events; published to an mqtt broker in a known format
 - anomalous sound events; CEPengine has a Noldus Communication Frame interface 
   to which sound sensors can post events in a known format
 - facecount events;  CEPengine has a http interface to which face counting
   cameras can post events in a known format

CEPengine and the mqtt broker make themselves known using mDNS/DNS-SD.

Marc de Lignie, Politie IV-organisatie, COMMIT/
September 9, 2014
"""

import java.lang
import time, sys, threading, urllib, urllib2
import paho, jycep, httpsensors, mqttsensors, ncfsensors, eventgenerator
import paho  # Python wrapper for mqtt-client-0.4.0.jar
from ncfsensors import ANOMALOUS_SOUND

ENGINEURI = "CEPengine"
HTTPSENSOR_PORT = 3433
HTTPSENSOR_URL = 'http://localhost:' + str(HTTPSENSOR_PORT) + '/sensafety'
NCFHOST = 'localhost'
NCFPORT = 5672
NCFUSERNAME = 'guest'
NCFPASSWORD = 'guest'
NCFVIRTUALHOST = ""
NCFSOUND_EXCHANGE = 'SenSafety_Sweet'

SILENT = 'Silent'
BUSY = 'Busy'

# WebMonitor URLs
URL_SOUND = 'http://localhost:8555/SenSafety_MidTerm/eventdb/sound'
URL_FACE = 'http://localhost:8555/SenSafety_MidTerm/eventdb/face'
URL_TILT = 'http://localhost:8555/SenSafety_MidTerm/eventdb/tilt'
URL_SILENT = 'http://localhost:8555/SenSafety_MidTerm/eventdb/silent'
URL_BUSY = 'http://localhost:8555/SenSafety_MidTerm/eventdb/busy'

# URL where Ambient pushes mqtt events (does not allow publish?)
# MQTT_BROKER_URL = "tcp://vps38114.public.cloudvps.com:1883"
# Can be used locally together with mqtt generator(s)
# MQTT_BROKER_URL = "tcp://localhost:1883"
# Can be used from the cloud when using the mqtt event generator
MQTT_BROKER_URL = "tcp://m2m.eclipse.org:1883"


class CEPengine(object):

    def __init__(self):
        self._cep = jycep.EsperEngine(ENGINEURI)
        #try: Future work: plug and play setup with Avahi
        #    self._avahiBrowse() # Presently not used by CEPengine
        #except:
        #    print "No avahi-daemon running on localhost"
        try:
            self.pahoclient = paho.PahoClient(MQTT_BROKER_URL)
            mqttsensors.MqttTiltSensor(self._cep, self.pahoclient)
            # mqttsensors.MqttContactSensor(self._cep, self.pahoclient)
        except:
            print "No mqtt broker listening on localhost port 1883"
        httpsensors.HttpSensors(self._cep, ENGINEURI, HTTPSENSOR_PORT)
        self.NcfSoundSensor = ncfsensors.NcfSoundSensor(self._cep, 
                NCFHOST, NCFPORT, NCFUSERNAME, NCFPASSWORD, 
                NCFVIRTUALHOST, NCFSOUND_EXCHANGE)
        qman = QueryManager(self._cep)
        qman.addQuery(QueryAnomalousSound())  
        qman.addQuery(QueryFacecount())  
        qman.addQuery(QueryTilt())  
        # qman.addQuery(QueryContact())  Not used for MidTerm demo
       
    """def _avahiBrowse(self):
        # Future work: plug and play setup with Avahi
        # Get zeroconf info for connection with Mqtt broker
        b1 = avahi.ServiceBrowser("_mqtt._tcp")
        time.sleep(1) # Time delay for browsing services
        self._mqttservices = b1.getServices()
        if len(self._mqttservices) == 0:
            print "No mqtt broker advertized with mDNS/DNS-SD"
            print "    Assuming mosquitto service on " + MQTT_BROKER_URL
        else:
            print "mqtt service(s):\n", self._mqttservices
        # Get zeroconf info for connection with Cocoon gateways
        # Just for now; only relevant for the situation awareness portal
        b2 = avahi.ServiceBrowser("_cocoon._tcp")
        time.sleep(1) # Time delay for browsing services
        self._cocoonservices = b2.getServices()
        if len(self._cocoonservices) == 0:
            print "No Cocoon service advertized with mDNS/DNS-SD"
        else:
            print "Cocoon service(s):\n", self._cocoonservices"""
        

class QueryManager(object):
    # EPL queries are based on the Esper 4.9.0 Reference

    def __init__(self, cep):
        self._cep = cep

    def addQuery(self, queryobject):
        try:
            (eventtype, eventfields) = queryobject.getResultEvent()
            self._cep.define_event(eventtype, eventfields)
        except  AttributeError:
            pass    # Event definitions absent for filtering queries
        for query in queryobject.getQueries(): 
            stmt = self._cep.create_query(query)
            stmt.addListener(jycep.EventListener(queryobject.listener))
 

class QueryAnomalousSound(object):

    def getQueries(self):
        return ['select * from %s' % ANOMALOUS_SOUND]

    def listener(self, data_new, data_old):
        if not isinstance(data_new, list):
            data_new = [data_new]
        for item in data_new:
            print 'Anomalous sound event passed through CEPengine:\n', \
                  str(item)[:160]
            # Post to Web monitor
            eventdata = {
                'mac': item['MAC'],
                'timestamp': item['timestamp'],
                'soundlevel': item['probability']}
            eventurl = URL_SOUND + urllib.urlencode(eventdata)
            urllib2.urlopen(eventurl)


class QueryFacecount(object):

# Define in httpsensors.py
#    def getResultEvent(self):
#        return (httpsensors.FACECOUNT, {
#            'mac': java.lang.String,
#            'timestamp': java.lang.String, # ISO 8601
#            'facecount': java.lang.Float })

    def getQueries(self):
        return ['select * from %s' % httpsensors.FACECOUNT]

    def listener(self, data_new, data_old):
        if not isinstance(data_new, list):
            data_new = [data_new]
        for item in data_new:
            print 'Facecount event passed through CEPengine:\n', \
                  str(item)[:160]
            # Post to Web monitor
            eventdata = {
                'mac': item['mac'],
                'timestamp': item['timestamp'],
                'facecount': item['facecount']}
            urllib2.urlopen(URL_FACE, urllib.urlencode(eventdata))

""" Event generator sends directly to WebMonitor
class QuerySilent(object):

    def getResultEvent(self):
        return (SILENT, {
            'dataset': java.lang.String,
            'timestamp': java.lang.String, # ISO 8601
            'facecount': java.lang.Integer })

    def getQueries(self):
        return ['select * from %s' % SILENT]

    def listener(self, data_new, data_old):
        if not isinstance(data_new, list):
            data_new = [data_new]
        for item in data_new:
            print 'Silent event passed through CEPengine:\n', \
                  str(item)[:160]
            # Post to Web monitor
            eventdata = {
                'location': item['location'],
                'timestamp': item['timestamp'],
                'facecount': item['facecount'],
                'soundlevel': item['silent']}
            eventurl = URL_SILENT + urllib.urlencode(eventdata)
            urllib2.urlopen(eventurl)
"""

class QueryTilt(object):

    def getQueries(self):
        return ['select * from %s' % mqttsensors.TILT]

    def listener(self, data_new, data_old):
        if not isinstance(data_new, list):
            data_new = [data_new]
        for item in data_new:
            print 'Tilt event passed through CEPengine:\n', str(item)[:320]
            # Post to Web monitor
            eventdata = {
                'sensor_id': item['sensor_id'],
                'timestamp': item['timestamp'],
                'event': item['event'],
                'state': item['state']}
            urllib2.urlopen(URL_TILT, urllib.urlencode(eventdata))
            

class QueryContact(object):
    # For now: just print incoming events after passing through the cep engine

    def getQueries(self):
        return ['select * from %s' % mqttsensors.CONTACT]

    def listener(self, data_new, data_old):
        if not isinstance(data_new, list):
            data_new = [data_new]
        for item in data_new:
            print 'Contact event passed through CEPengine:\n', str(item)[:320]


if __name__ == "__main__":
    cep = CEPengine()
    # Random events for initial testing
#    soundevents = eventgenerator.AnomalousSound(30, NCFSOUND_EXCHANGE)
#    soundevents.start()
    faceevents = eventgenerator.Facecount(HTTPSENSOR_URL, 7)
    faceevents.start()
#    tiltevents = eventgenerator.Tilt(cep.pahoclient, 30)
#    tiltevents.start()
#    silentevents = eventgenerator.Silent(URL_SILENT, 30) 
#    silentevents.start()
#    busyevents = eventgenerator.Busy(URL_BUSY, 30) 
#    busyevents.start()
#    ilpevents = eventgenerator.ILP_control(cep.pahoclient, 30)
#    ilpevents.start()
    time.sleep(300)
#    soundevents.stop()
    faceevents.stop()
#    tiltevents.stop()
#    silentevents.stop()
#    busyevents.stop()
#    ilpevents.stop()
    cep.pahoclient.close()  # Required for jython to exit
   


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
September 24, 2014
"""

import time, sys, threading
import jycep, httpsensors, mqttsensors, ncfsensors, ilpcontrol, eventgenerator
from queries import QueryAnomalousSound, QueryFacecount, QueryCountSounds, \
                    QueryBusy, QueryTilt
import paho  # Python wrapper for mqtt-client-0.4.0.jar

ENGINEURI = "CEPengine"
HTTPSENSOR_PORT = 3433
HTTPSENSOR_URL = 'http://localhost:' + str(HTTPSENSOR_PORT) + '/sensafety'
NCFHOST = 'localhost'
NCFPORT = 5672
NCFUSERNAME = 'guest'
NCFPASSWORD = 'guest'
NCFVIRTUALHOST = '/'
NCFSOUND_EXCHANGE = 'sensors_meta_data' #'SenSafety_Sweet'

TBATCH = 60           # Batch window for CountSounds and AvgFacecount
BUSYTHRESHOLD = 100   # Config QueryBusy
BUSYTIMEOUT = 60      # Change interval busy level

# URL where Ambient pushes mqtt events (does not allow publish)
MQTT_BROKER_AMBIENT = "tcp://vps38114.public.cloudvps.com:1883"

# URL to be used locally for publishing mqtt messages
MQTT_BROKER_LOCAL = "tcp://localhost:1883"


class CEPengine(object):

    def __init__(self):
        self._cep = jycep.EsperEngine(ENGINEURI)
        #try: Future work: plug and play setup with Avahi
        #    self._avahiBrowse() # Presently not used by CEPengine
        #except:
        #    print "No avahi-daemon running on localhost"
        try:
            self.pahoclient_ambient = paho.PahoClient(MQTT_BROKER_AMBIENT)
            mqttsensors.MqttTiltSensor(self._cep, self.pahoclient_ambient)
        except:
            print "Ambient mqtt broker not available"
        httpsensors.HttpSensors(self._cep, ENGINEURI, HTTPSENSOR_PORT)
        self.NcfSoundSensor = ncfsensors.NcfSoundSensor(self._cep, 
                NCFHOST, NCFPORT, NCFUSERNAME, NCFPASSWORD, 
                NCFVIRTUALHOST, NCFSOUND_EXCHANGE)
        qman = QueryManager(self._cep)
        q = QueryAnomalousSound()
        qman.addQuery(q.getQueries(), q.listener)  
        q = QueryCountSounds(TBATCH)
        qman.addQuery(q.getQueries(), q.listener)  
        q = QueryFacecount(TBATCH)
        qman.addQuery(q.getQueries(), q.listener) 
        q = QueryBusy(BUSYTHRESHOLD) 
        qman.addQuery(q.getQueries(), q.listener, q.getResultEvent())  
        q = QueryTilt()
        qman.addQuery(q.getQueries(), q.listener)  
        # qman.addQuery(QueryContact())  Not used for MidTerm demo
        try:
            self.pahoclient_local = paho.PahoClient(MQTT_BROKER_LOCAL)
        except:
            print "Local mqtt broker not available"
        self.ilpclient = ilpcontrol.ILPControl(
                                    self.pahoclient_local, BUSYTIMEOUT)
       
    """ Commented out for MidTerm event
        def _avahiBrowse(self):
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

    def addQuery(self, queries, listener, resultevent=None):
        try:
            (eventtype, eventfields) = resultevent
            self._cep.define_event(eventtype, eventfields)
        except TypeError:
            pass    # Event definitions absent for filtering queries
        for query in queries: 
            stmt = self._cep.create_query(query)
            stmt.addListener(jycep.EventListener(listener))
 

if __name__ == "__main__" and sys.argv[1] == 'sensing':  # During MidTerm event
    cep = CEPengine()
    while True:   # Do nothing until CTRL+C keyboard interrupt
        time.sleep(3000)
    cep.pahoclient_local.close()  # Required for jython to exit
    cep.pahoclient_ambient.close()  # Required for jython to exit
   
elif __name__ == "__main__" and sys.argv[1] == 'generate':  # For testing
    TBATCH = 10
    MQTT_BROKER_AMBIENT = "tcp://m2m.eclipse.org:1883"
    cep = CEPengine()
    soundevents = eventgenerator.AnomalousSound(3, NCFSOUND_EXCHANGE)
    soundevents.start()
    faceevents = eventgenerator.Facecount(HTTPSENSOR_URL, 7)
    faceevents.start()
    tiltevents = eventgenerator.Tilt(cep.pahoclient_ambient, 5)
    tiltevents.start()
#    ilpevents = eventgenerator.ILP(cep.pahoclient_local, 30, cep.ilpclient)
#    ilpevents.start()
    while True:   # Do nothing until CTRL+C keyboard interrupt
        time.sleep(3000)
    soundevents.stop()
    faceevents.stop()
    tiltevents.stop()
#    ilpevents.stop()
    cep.pahoclient_local.close()  # Required for jython to exit
    cep.pahoclient_ambient.close()  # Required for jython to exit
   


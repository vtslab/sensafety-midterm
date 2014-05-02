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
 - anomalous sound events; CEPengine has a http interface to which sound
   sensors can post events in a known format
 - face count events;  CEPengine has a http interface to which face counting
   cameras can post events in a known format

CEPengine and the mqtt broker make themselves known using mDNS/DNS-SD.

Marc de Lignie, Politie IV-organisatie, COMMIT/
May 2, 2014
"""

import java.lang
import time, sys
import avahi, paho, jycep, httpsensors, mqttsensors, eventgenerator

ENGINEURI = "CEPengine"
SERVICENAME = "sensafety"
ANOMALOUS_SOUND = 'AnomalousSound'
ANOMALOUS_SOUND_PORT = 33433
ANOMALOUS_SOUND_URL = 'http://localhost:' + str(ANOMALOUS_SOUND_PORT) +\
                      '/' + SERVICENAME
TILT = 'Tilt'
MQTT_BROKER_URL = "tcp://localhost:1883"


class CEPengine(object):

    def __init__(self):
        self._cep = jycep.EsperEngine(ENGINEURI)
        self._avahiBrowse() # Not actually used by CEPengine
        # Todo: get mqtt broker url from avahi
        self.pahoclient = paho.PahoClient(MQTT_BROKER_URL)
        httpsensors.HttpSensors(self._cep, ENGINEURI, ANOMALOUS_SOUND_URL, 
                                ANOMALOUS_SOUND_PORT)
        mqttsensors.MqttSensors(self._cep, self.pahoclient)
        qman = QueryManager(self._cep)
        qman.addQuery(QueryAnomalousSound())  
       
    def _avahiBrowse(self):
        # Get zeroconf info for connection with Mqtt broker
        b1 = avahi.ServiceBrowser("_mqtt._tcp")
        time.sleep(1) # Time delay for browsing services
        self._mqttservices = b1.getServices()
        if len(self._mqttservices) == 0:
            print "No mqtt broker advertized with mDNS/DNS-SD"
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
            print "Cocoon service(s):\n", self._cocoonservices
        

class QueryManager(object):
    # EPL queries are based on the Esper 4.9.0 Reference

    def __init__(self, cep):
        self.cep = cep
    
    def addQuery(self, queryobject):
        for query in queryobject.getQueries(): 
            stmt = self.cep.create_query(query)
            stmt.addListener(jycep.EventListener(queryobject.listener))
 

class QueryAnomalousSound(object):
    # For now: just print incoming events after passing through the cep engine

    def getQueries(self):
        return ['select * from %s' % ANOMALOUS_SOUND]

    def listener(self, data_new, data_old):
        if not isinstance(data_new, list):
            data_new = [data_new]
        for item in data_new:
            print 'Anomalous sound: ', str(item)[:160]


class QueryTilt(object):
    # For now: just print incoming events after passing through the cep engine

    def getQueries(self):
        return ['select * from %s' % TILT]

    def listener(self, data_new, data_old):
        if not isinstance(data_new, list):
            data_new = [data_new]
        for item in data_new:
            print 'Tilt: ', str(item)[:160]


if __name__ == "__main__":
    cep = CEPengine()
    # Random events for initial testing
    eventgenerator.AnomalousSound(ANOMALOUS_SOUND_URL, 3).start()
    eventgenerator.Tilt(cep.pahoclient, 3).start()
    time.sleep(10)
    cep.pahoclient.close()  # Required for jython to exit
   


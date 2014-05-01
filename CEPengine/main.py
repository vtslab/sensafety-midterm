#!/usr/bin/env jython

# SenSafety.MidTerm.CEPengine provides the Esper based complex event processing
# engine for the mid-term SenSafety demo. It:
#  - activates the Esper CEP engine and registers recognized event types
#    (module CEP engine.py)
#  - provides http input to sensors that post events of a recognized type
#    (module httpsensors.py)
#  - searches the local network for mqtt brokers and subscribes to events
#    of a recognized type (mqttsensors.py)
#  - registers queries for higher-level events (module queries.py)
#  - posts all incoming and inferred events to the situation awareness portal
#    (module CEP engine.py)

# It should be run with the CEPengine.sh shell script, which defines
# the jython classpath and sets the virtualenv environment

# Marc de Lignie, Politie IV-organisatie, COMMIT/
# April 18, 2014

import java.lang

import time, sys
import avahi, jycep, httpsensors, eventgenerator

ENGINEURI = "CEPengine"
SERVICENAME = "sensafety"
ANOMALOUS_SOUND = 'AnomalousSound'
ANOMALOUS_SOUND_PORT = 33433
ANOMALOUS_SOUND_URL = 'http://localhost:' + str(ANOMALOUS_SOUND_PORT) +\
                      '/' + SERVICENAME


class QueryAnomalousSound(object):

    def getQueries(self):
        return ['select * from %s' % ANOMALOUS_SOUND]

    def listener(self, data_new, data_old):
        if not isinstance(data_new, list):
            data_new = [data_new]
        for item in data_new:
            print 'Listener: ', str(item)[:160]


class CEPengine(object):

    def __init__(self):
        self._cep = jycep.EsperEngine(ENGINEURI)
        self._cep.define_event(ANOMALOUS_SOUND, { 
            'timestamp': java.lang.String, # ISO 8601:
                                           # 2014-04-10T11:22:33.44+02:00
            'geoNB': java.lang.Float,      # ISO 6709: 52.12345
            'geoEL': java.lang.Float,      # ISO 6709:  5.12345
            'MAC': java.lang.String,
            'probability': java.lang.Float })
        httpsensors.HttpSensors(ENGINEURI, ANOMALOUS_SOUND_URL, 
                                ANOMALOUS_SOUND_PORT, ANOMALOUS_SOUND)
        self._avahiBrowse()
        qman = QueryManager(self._cep)
        qman.addQuery(QueryAnomalousSound())  
       
    def _avahiBrowse(self):
        b1 = avahi.ServiceBrowser("_mqtt._tcp")
        time.sleep(1) # Time delay for browsing services
        self._mqttservices = b1.getServices()
        if len(self._mqttservices) == 0:
            print "No mqtt service found"
        else:
            print "mqtt service(s):\n", self._mqttservices
        b2 = avahi.ServiceBrowser("_cocoon._tcp")
        time.sleep(1) # Time delay for browsing services
        self._cocoonservices = b2.getServices()
        if len(self._mqttservices) == 0:
            print "No cocoon service found"
        else:
            print "mqtt service(s):\n", self._mqttservices
        

class QueryManager(object):
    # EPL queries are based on the Esper 4.9.0 Reference

    def __init__(self, cep):
        self.cep = cep
    
    def addQuery(self, queryobject):
        for query in queryobject.getQueries(): 
            stmt = self.cep.create_query(query)
            stmt.addListener(jycep.EventListener(queryobject.listener))
 

if __name__ == "__main__":
    cep = CEPengine()
    # Random events for initial testing
    eventgenerator.AnomalousSound(ANOMALOUS_SOUND_URL, 3).start()
    eventgenerator.Tilt().start()
   




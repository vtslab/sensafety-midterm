#!/usr/bin/env jython

# SenSafety.MidTerm.CEPengine provides the Esper based complex event processing
# engine for the mid-term SenSafety demo. 
# The module httpsensors provides http input to sensors that post events of a 
# registered type

# Marc de Lignie, Politie IV-organisatie
# August 29, 2014


import java.lang
import time, random, threading
from com.espertech.esperio.http import EsperIOHTTPAdapter
from com.espertech.esperio.http.config import ConfigurationHTTPAdapter
from com.espertech.esperio.http.config import Service
from com.espertech.esperio.http.config import GetHandler

ANOMALOUS_SOUND = 'AnomalousSound'
FACECOUNT = 'Facecount'


class HttpSensors(object):

    eventtypes = {
        'AnomalousSound':    { 
            'timestamp': java.lang.String, # ISO 8601:
                                           # 2014-04-10T11:22:33.44+02:00
            'geoNB': java.lang.Float,      # ISO 6709: 52.12345
            'geoEL': java.lang.Float,      # ISO 6709:  5.12345
            'MAC': java.lang.String,
            'probability': java.lang.Float },
        }

    def __init__(self, cep, engineURI, url, port):
        self._cep = cep
        self._registerHttpEvents(self.eventtypes)
        self._httpAdapter = self._constructHttpAdapter(engineURI, port)
        self._httpAdapter.start()
        
    def _registerHttpEvents(self, eventtypes):
        for eventtype in self.eventtypes.keys():
            self._cep.define_event(eventtype, self.eventtypes[eventtype])
        
    def _constructHttpAdapter(self, engineURI, port):
        service = Service()
        service.setPort(port)
        service.setNio(False)
        gethandler = GetHandler()
        gethandler.setService('sensafety')
        gethandler.setPattern('*')
        adapterConfig = ConfigurationHTTPAdapter()
        adapterConfig.setServices({'sensafety': service})
        adapterConfig.setGetHandlers([gethandler])
        return EsperIOHTTPAdapter(adapterConfig, engineURI)


class Facecount(threading.Thread):
    """
    Facecount will poll facecount events from a web server.
    The current implementation only acts as event generator.
    """

    def __init__(self, cep, interval):
        threading.Thread.__init__(self)
        self._cep = cep
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
        eventdata = {
            'timestamp': '2014-04-10T11:22:33.44+02:00', # ISO 8601
            'dataset': 'eventgenerator',
            'facecount': 8 }
        self._cep.send_event(eventdata, FACECOUNT)
        #print 'Facecount event posted'

     


#!/usr/bin/env jython

# SenSafety.MidTerm.CEPengine provides the Esper based complex event processing
# engine for the mid-term SenSafety demo. 
# The module httpsensors provides http input to sensors that post events of a 
# registered type

# Marc de Lignie, Politie IV-organisatie
# September 24, 2014


import java.lang
import time, random, threading
from com.espertech.esperio.http import EsperIOHTTPAdapter
from com.espertech.esperio.http.config import ConfigurationHTTPAdapter
from com.espertech.esperio.http.config import Service
from com.espertech.esperio.http.config import GetHandler
from queries import FACECOUNT

HTTPSENSOR_SERVICE = "sensafety"  # Only used within the CEPengine
HTTPSENSOR_PATTERN = "*"          # Accepts any url


class HttpSensors(object):

    eventtypes = {
        FACECOUNT:    { 
            'timestamp': java.lang.String, # ISO 8601
            'cam': java.lang.String,
            'facecount': java.lang.Float }
        }

    def __init__(self, cep, engineURI, port):
        self._cep = cep
        self._registerHttpEvents(self.eventtypes)
        self._httpAdapter = self._constructHttpAdapter(engineURI, port)
        self._httpAdapter.start()
        
    def _registerHttpEvents(self, eventtypes):
        for eventtype in self.eventtypes.keys():
            self._cep.define_event(eventtype, self.eventtypes[eventtype])
            print eventtype + ' sensor initialized (HTTP)'
        
    def _constructHttpAdapter(self, engineURI, port):
        service = Service()
        service.setPort(port)
        service.setNio(False)
        gethandler = GetHandler()
        gethandler.setService(HTTPSENSOR_SERVICE)
        gethandler.setPattern(HTTPSENSOR_PATTERN)
        adapterConfig = ConfigurationHTTPAdapter()
        adapterConfig.setServices({HTTPSENSOR_SERVICE: service})
        adapterConfig.setGetHandlers([gethandler])
        return EsperIOHTTPAdapter(adapterConfig, engineURI)


     

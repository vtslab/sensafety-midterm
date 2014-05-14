#!/usr/bin/env jython

# SenSafety.MidTerm.CEPengine provides the Esper based complex event processing
# engine for the mid-term SenSafety demo. 
# The module httpsensors provides http input to sensors that post events of a 
# registered type

# Marc de Lignie, Politie IV-organisatie
# April 10, 2014


import java.lang
from com.espertech.esperio.http import EsperIOHTTPAdapter
from com.espertech.esperio.http.config import ConfigurationHTTPAdapter
from com.espertech.esperio.http.config import Service
from com.espertech.esperio.http.config import GetHandler


class HttpSensors(object):

    eventtypes = {
        'AnomalousSound':    { 
            'timestamp': java.lang.String, # ISO 8601:
                                           # 2014-04-10T11:22:33.44+02:00
            'geoNB': java.lang.Float,      # ISO 6709: 52.12345
            'geoEL': java.lang.Float,      # ISO 6709:  5.12345
            'MAC': java.lang.String,
            'probability': java.lang.Float },
        'FaceCount': { 
            'timestamp': java.lang.String # ISO 8601:
                                           # 2014-04-10T11:22:33.44+02:00
            }
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



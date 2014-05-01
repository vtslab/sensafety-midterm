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


""" For initial testing main.py defines a variant stream that accepts anything
eventtypes = {
    'AnomalousSound': { 
        'name': java.lang.String,
        'cam': java.lang.String,
        'ddate': java.lang.String,
        'ttime': java.lang.String,
        'millisec': java.lang.Long,
        'foto': java.lang.String
        },
    'FaceCount': { 
        'name': java.lang.String,
        'cam': java.lang.String,
        'ddate': java.lang.String,
        'ttime': java.lang.String,
        'millisec': java.lang.Long,
        'foto': java.lang.String
        }
    }"""


class HttpSensors(object):

    def __init__(self, engineURI, url, port, eventtype):
#        self._cep = cep
#        self._registerHttpEvents(eventtypes)
        self._httpAdapter = self._constructHttpAdapter(
                                engineURI, url, port, eventtype)
        self._httpAdapter.start();
        
#    def _registerHttpEvents(self, eventtypes):
#        for eventtype in eventtypes.keys():
#            self._cep.define_event(eventtype, eventtypes[eventtype])
        
    def _constructHttpAdapter(self, engineURI, url, port, eventtype):
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



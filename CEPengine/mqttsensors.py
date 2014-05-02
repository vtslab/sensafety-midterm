#!/usr/bin/env jython

# SenSafety.MidTerm.CEPengine provides the Esper based complex event processing
# engine for the mid-term SenSafety demo. 
# This module provides mqtt input to sensors that post events of a 
# registered type

# Marc de Lignie, Politie IV-organisatie
# May 2, 2014

import java.lang
import paho


eventspecs = {
    'Tilt': {
        'fields': {
            'timestamp': java.lang.String, # ISO 8601:
                                           # 2014-04-10T11:22:33.44+02:00
            'previous_timestamp': java.lang.String,
            'event': java.lang.String,
            'state': java.lang.String },
        'topicfilter': '#',
        'callback': 'tiltCallback'},
    'Breach': { 
        'fields': {
            'timestamp': java.lang.String, # ISO 8601:
                                           # 2014-04-10T11:22:33.44+02:00
            'source': java.lang.String,
            'switch_state': java.lang.Boolean },
        'topicfilter': '#',
        'callback': 'breachCallback'}
    }


class MqttSensors(object):

    def __init__(self, cep, pahoclient):
        self._cep = cep
        self._pahoclient = pahoclient
        self._registerMqttEvents()
        
    def _registerMqttEvents(self):
        for eventtype in eventspecs.keys():
            self._cep.define_event(eventtype, eventspecs[eventtype]['fields'])
            topicfilter = eventspecs[eventtype]['topicfilter']
            callback = eventspecs[eventtype]['callback']
            self._pahoclient.subscribe(topicfilter, 1, eval('self.'+callback))
        
    def tiltCallback(self, message):
        print 'Tilt: ' + message
    
    def breachCallback(self, message):
        print 'Breach: ' + message

"""
public static Document loadXMLFromString(String xml) throws Exception
{
    DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
    DocumentBuilder builder = factory.newDocumentBuilder();
    InputSource is = new InputSource(new StringReader(xml));
    return builder.parse(is);
}
"""

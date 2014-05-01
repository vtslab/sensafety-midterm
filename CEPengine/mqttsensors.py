#!/usr/bin/env jython

# SenSafety.MidTerm.CEPengine provides the Esper based complex event processing
# engine for the mid-term SenSafety demo. 
# This module provides mqtt input to sensors that post events of a 
# registered type

# Marc de Lignie, Politie IV-organisatie
# April 7, 2014

import paho

eventtypes = {
    'Tilt': { 
        'name': java.lang.String,
        'cam': java.lang.String,
        'ddate': java.lang.String,
        'ttime': java.lang.String,
        'millisec': java.lang.Long,
        'foto': java.lang.String
        },
    'Breach': { 
        'name': java.lang.String,
        'cam': java.lang.String,
        'ddate': java.lang.String,
        'ttime': java.lang.String,
        'millisec': java.lang.Long,
        'foto': java.lang.String
        },
    }


class MqttSensors(object):

    def __init__(self, cep, eventtypes, broker):
        self._cep = cep
        self._registerMqttEvents(eventtypes)
        self._mqttAdapter = self._constructMqttAdapter(engineURI, port)
        self._mqttAdapter.start();
        
    def _registerMqttEvents(self, eventtypes):
        for eventtype in eventtypes.keys():
            self._cep.define_event(eventtype, eventtypes[eventtype])
        
    def _constructMqttAdapter(self):
        return paho.MqttClient(adapterConfig, engineURI)


    

    String url = protocol + broker + ":" + port


    sampleClient = Sample(url, clientId, cleanSession, quietMode,userName,password)
    # if (action.equals("publish")) 
        sampleClient.publish(topic,qos,message.getBytes())
    # else if (action.equals("subscribe")) 
        sampleClient.subscribe(topic,qos)
    

"""
public static Document loadXMLFromString(String xml) throws Exception
{
    DocumentBuilderFactory factory = DocumentBuilderFactory.newInstance();
    DocumentBuilder builder = factory.newDocumentBuilder();
    InputSource is = new InputSource(new StringReader(xml));
    return builder.parse(is);
}
"""

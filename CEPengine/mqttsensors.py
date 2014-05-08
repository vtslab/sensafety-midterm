#!/usr/bin/env jython

# SenSafety.MidTerm.CEPengine provides the Esper based complex event processing
# engine for the mid-term SenSafety demo. 
# This module provides mqtt input to sensors that post events of a 
# registered type

# Marc de Lignie, Politie IV-organisatie
# May 8, 2014

import java.lang
from java.io import StringReader
from javax.xml.parsers import DocumentBuilderFactory, DocumentBuilder
from org.xml.sax import InputSource
from org.w3c.dom import Node

MQTTQOS = 1
TILTTOPIC = 'tilt'  #'owner/net_id/class/sub_class/function/type/device_id'
BREACHTOPIC = 'breach'  #'owner/net_id/class/sub_class/function/type/device_id'


class MqttTiltSensor(object):

    eventspecs = {
        'type': 'Tilt',
        'fields': {
            'timestamp': java.lang.String, # ISO 8601:
                                           # 2014-04-10T11:22:33.44+02:00
            'previous_timestamp': java.lang.String,
            'event': java.lang.String,
            'state': java.lang.String }
        }

    def __init__(self, cep, pahoclient):
        self._cep = cep
        self._cep.define_event(self.eventspecs['type'], 
                               self.eventspecs['fields'])
        pahoclient.subscribe(TILTTOPIC, MQTTQOS, self.tiltCallback)
        
    def tiltCallback(self, message):      
        try:
            tiltEvent = {}
            builder = DocumentBuilderFactory.newInstance().newDocumentBuilder()
            topnode = builder.parse(InputSource(StringReader((
                                   message.toString())))).getFirstChild()
            assert topnode.getNodeName() == 'Payload'
            nodes1lev = topnode.getChildNodes()
            for i in xrange(nodes1lev.getLength()):
                node1 = nodes1lev.item(i)
                assert node1.getNodeName() == 'Parameter'
                atts = node1.getAttributes()
                tiltEvent[atts.item(0).getNodeValue()] = node1.getTextContent()
        except Exception, e:
            print "Error in SenSafety/mqtt xml format, " + str(e)
        self._cep.send_event(tiltEvent, "Tilt")
    

class MqttBreachSensor(object):

    eventspecs = {
        'type': 'Breach',
        'fields': {
            'timestamp': java.lang.String, # ISO 8601:
                                           # 2014-04-10T11:22:33.44+02:00
            'source': java.lang.String,
            'switch_state': java.lang.Boolean }
        }

    def __init__(self, cep, pahoclient):
        self._cep = cep
        self._cep.define_event(self.eventspecs['type'], 
                               self.eventspecs['fields'])
        pahoclient.subscribe(BREACHTOPIC, MQTTQOS, self.breachCallback)
        
    def breachCallback(self, message):
        print 'Breach: ' + message.toString()




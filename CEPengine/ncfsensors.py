#!/usr/bin/env jython

# SenSafety.MidTerm.CEPengine provides the Esper based complex event processing
# engine for the mid-term SenSafety demo. 
# The module ncfsensors provides input from sensors that post events using the
# Noldus Communication Framework

# Marc de Lignie, Politie IV-organisatie
# September 26, 2014

import java.lang
import sys, time
sys.path.append('/home/m-doit/Python/SenSafety/MidTerm/site-packages') 
import simplejson as json
import nl.noldus.nmf.NCNmfConsumer as NCNmfConsumer
import nl.noldus.nmf.NCNmfTypes as NCNmfTypes
import nl.noldus.nmf.NINmfConsumeString as NINmfConsumeString
import nl.noldus.nmf.NINmfShutdown as NINmfShutdown
from queries import ANOMALOUS_SOUND

class NcfSoundSensor(NINmfConsumeString, NINmfShutdown) :

    eventspecs = {
        'type': ANOMALOUS_SOUND,
        'fields': {
            'timestamp': java.lang.String,
            'mac': java.lang.String,
            'soundlevel': java.lang.String }
        }

    def __init__(self, cep, HOST, PORT, USERNAME, PASSWORD,
                       VIRTUALHOST, SOUND_EXCHANGE):
        self._cep = cep
        self._cep.define_event(self.eventspecs['type'], 
                               self.eventspecs['fields'])
        self.consumer = NCNmfConsumer()
        self.consumer.SetOnConsumeString(self)
        self.consumer.SetOnShutdown(self)
        self.consumer.Open(HOST, PORT, USERNAME, PASSWORD, VIRTUALHOST)
        # Bind to the specified Exchange and create an anonymous queue.
        self.consumer.Bind(NCNmfTypes.EExchangeType.eExchangeTypeFanout, 
                           SOUND_EXCHANGE, "", "")
        print 'Sound sensors initialized (NCF AMQP)'
    
    def OnConsumeString(self, jsonstr): 
        eventin = json.loads(jsonstr)
        event = {
            'mac': eventin['id'],
            'soundlevel': eventin['soundLevel'],
            'timestamp': time.strftime("%Y-%m-%dT%H:%M:%S", 
                                       time.localtime(time.time()))
            }
        self._cep.send_event(event, self.eventspecs['type'])

    def OnShutdown(self):
        pass
        

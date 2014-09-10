#!/usr/bin/env jython

# SenSafety.MidTerm.CEPengine provides the Esper based complex event processing
# engine for the mid-term SenSafety demo. 
# The module ncfsensors provides input from sensors that post events using the
# Noldus Communication Framework

# Marc de Lignie, Politie IV-organisatie
# September 8, 2014

import java.lang
import sys
sys.path.append('site-packages') 
import simplejson as json
import nl.noldus.nmf.NCNmfConsumer as NCNmfConsumer
import nl.noldus.nmf.NCNmfTypes as NCNmfTypes
import nl.noldus.nmf.NINmfConsumeString as NINmfConsumeString
import nl.noldus.nmf.NINmfShutdown as NINmfShutdown

ANOMALOUS_SOUND = 'Anomalous_Sound'


class NcfSoundSensor(NINmfConsumeString, NINmfShutdown) :

    eventtypes = {
        ANOMALOUS_SOUND:    { 
            'message': java.lang.String,
            'id': java.lang.String,
            'soundLevel': java.lang.String }
        }

    def __init__(self, cep, HOST, PORT, USERNAME, PASSWORD,
                       VIRTUALHOST, SOUND_EXCHANGE):
        self._cep = cep
        self._registerNcfEvents(self.eventtypes)
        self.consumer = NCNmfConsumer()
        self.consumer.SetOnConsumeString(self)
        self.consumer.SetOnShutdown(self)
        self.consumer.Open(HOST, PORT, USERNAME, PASSWORD, VIRTUALHOST)
        # Bind to the specified Exchange and create an anonymous queue.
        self.consumer.Bind(NCNmfTypes.EExchangeType.eExchangeTypeFanout, 
                           SOUND_EXCHANGE, "", "")
        print 'Sound sensors initialized (NCF AMQP)'
    
    def _registerNcfEvents(self, eventtypes):
        for eventtype in self.eventtypes.keys():
            self._cep.define_event(eventtype, self.eventtypes[eventtype])
     
    def OnConsumeString(self, jsonstr): 
        print json.loads(jsonstr)

    def OnShutdown(self):
        pass
        

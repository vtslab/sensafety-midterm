#!/usr/bin/env jython
# Test cases for queries.py, to be run with testqueries.sh (nosetests)

# Use the test framework for new queries or else you do not know what 
# EPL is doing and you are wasting time.

# Marc de Lignie, Politie IV-organisatie
# September 24, 2014

import java.lang
import sys, time, re
from mock import Mock
from jycep import EsperEngine
from jycep import EventListener
import queries

class QueryManager(object):
    # EPL queries are based on the Esper 4.9.0 Reference

    def __init__(self, cep):
        self._cep = cep

    def addQuery(self, queries, listener):
        for query in queries: 
            stmt = self._cep.create_query(query)
            stmt.addListener(EventListener(listener))
 

#Avg Facecount
"""Maak een gemiddelde eens per minuut van 15 events.
insert into AvgFacecount
select avg(facecount) as fc from Facecount.win:time_batch(60 sec)"""

class TestQueryFacecount(object):
    def setup(self):   # Run independently for every testcast
        self.cep = EsperEngine("TestAvgFacecount")
        self.cep.define_event('Facecount', { 
            'timestamp': java.lang.String, # ISO 8601
            'mac': java.lang.String,
            'facecount': java.lang.Float }
            )
        self.cep.define_event('AvgFacecount', { 
            'facecount': java.lang.Float,
            'avgfacecount': java.lang.Double
            })
        self.mocklisten = Mock()
        self.qman = QueryManager(self.cep)
        qa = queries.QueryFacecount(4)
        self.qman.addQuery(qa.getQueries(), self.mocklisten)

            
    def testFacecount1(self):
    #Test AvgFacecount (met 0, 1 en 3 berichten)
        self.cep.send_event({
            'timestamp': '2014-07-07T11:22:33',
            'mac': 'macf',
            'facecount': 10.}, 'Facecount')
        time.sleep(5)
        self.cep.send_event({
            'timestamp': '2014-07-07T11:22:33',
            'mac': 'macf',
            'facecount': 1}, 'Facecount')
        self.cep.send_event({
            'timestamp': '2014-07-07T11:22:33',
            'mac': 'macf',
            'facecount': 3}, 'Facecount')
        self.cep.send_event({
            'timestamp': '2014-07-07T11:22:33',
            'mac': 'macf',
            'facecount': 8}, 'Facecount')
        time.sleep(4)
        print self.mocklisten.mock_calls
        # Possibly simpler with json.loads
        results = re.findall("avgfacecount': (.*?)}", 
                          str(self.mocklisten.mock_calls))
        assert results[0] == '10.0'
        assert results[2] == '4.0'


#SoundGroup
"""Sound alleen doorlaten als er geen ander sound event van hetzelfde device was
de afgelopen 2 seconden.
Coincidenties tussen soundgroups van verschillende devices zijn niet van belang.
insert into SoundGroup select * from pattern
	[every s1=sound1 -> (timer:interval(2 sec) and not s2=sound1 and s1.id=s2.id)]
"""

class TestQueryAnomalous(object):

    def setup(self):   # Run independently for every testcast
        self.cep = EsperEngine("TestAnomalous")
        self.cep.define_event('Anomalous_Sound', {
            'timestamp': java.lang.String,
            'mac': java.lang.String,
            'soundlevel': java.lang.String }
            )
        self.cep.define_event('SoundGroup', { 
            'timestamp': java.lang.String,
            'mac': java.lang.String,
            'soundlevel': java.lang.String }
            )
        self.mocklisten = Mock()
        self.qman = QueryManager(self.cep)
        qa = queries.QueryAnomalousSound()
        self.qman.addQuery(qa.getQueries(), self.mocklisten)

            
    def testAnomalous(self):
    #Test SoundGroup (mac1 wel msg1,msg3, geen msg2, mac2 wel msg1, msg2)
        self.cep.send_event({
            'timestamp': 'msg1',
            'mac': 'mac1',
            'soundlevel': '0.5'}, 'Anomalous_Sound')
        self.cep.send_event({
            'timestamp': 'msg1',
            'mac': 'mac2',
            'soundlevel': '0.6'}, 'Anomalous_Sound')
        time.sleep(2.1)
        self.cep.send_event({
            'timestamp': 'msg2',
            'mac': 'mac2',
            'soundlevel': '0.7'}, 'Anomalous_Sound')
        self.cep.send_event({
            'timestamp': 'msg2',
            'mac': 'mac1',
            'soundlevel': '0.8'}, 'Anomalous_Sound')
        time.sleep(0.1)
        self.cep.send_event({
            'timestamp': 'msg3',
            'mac': 'mac1',
            'soundlevel': '0.9'}, 'Anomalous_Sound')
        time.sleep(2.1)
        print self.mocklisten.mock_calls
        results = re.findall("soundlevel': u'(.*?)'", 
                          str(self.mocklisten.mock_calls))
        assert results[0] == '0.5'
        assert results[1] == '0.6' 
        assert results[2] == '0.7' 
        assert results[3] == '0.9'


#Sum SoundGroup
"""Maak een som eens per minuut van maximaal 30 events.
insert into Countsg1
select count(soundlevel) as Nsg1 from Soundgroup.win:time_batch(60 sec)
where mac=mac1

insert into Countsg2
select count(soundlevel) as Nsg2 from Soundgroup.win:time_batch(60 sec)
where mac=mac2"""

class testQueryCountSounds(object):
    
    TWIN = 4
    
    def setup(self):   # Run independently for every testcast
        self.cep = EsperEngine("TestCountSounds")
        self.cep.define_event('SoundGroup', { 
            'timestamp': java.lang.String,
            'mac': java.lang.String,
            'soundlevel': java.lang.String }
            )
        self.cep.define_event('CountSounds', { 
            'mac': java.lang.String,
            'nsg': java.lang.Long }
            )
        self.mocklisten = Mock()
        self.qman = QueryManager(self.cep)
        qa = queries.QueryCountSounds(self.TWIN)
        self.qman.addQuery(qa.getQueries(), self.mocklisten)

    def testCountSounds(self):
    #Test Countsounds (met 0, 1 en 3 events)
        time.sleep(self.TWIN + 0.5)
        self.cep.send_event({
            'timestamp': 'msg',
            'mac': 'mac1',
            'soundlevel': '0.5'}, 'SoundGroup')
        time.sleep(self.TWIN + 0.5)
        self.cep.send_event({
            'timestamp': 'msg',
            'mac': 'mac2',
            'soundlevel': '0.5'}, 'SoundGroup')
        self.cep.send_event({
            'timestamp': 'msg',
            'mac': 'mac1',
            'soundlevel': '0.5'}, 'SoundGroup')
        self.cep.send_event({
            'timestamp': 'msg',
            'mac': 'mac1',
            'soundlevel': '0.5'}, 'SoundGroup')
        self.cep.send_event({
            'timestamp': 'msg',
            'mac': 'mac1',
            'soundlevel': '0.5'}, 'SoundGroup')
        time.sleep(self.TWIN + 0.5)
        print self.mocklisten.mock_calls
        results = re.findall("nsg': (.*?)L", 
                          str(self.mocklisten.mock_calls))
        assert results[0] == '1'  # mac1 in second window
        assert results[1] == '0'  # mac1 out of first window
        
        assert results[2] == '1'  # mac2 in third window
        assert results[3] == '3'  # mac1 in third window
        assert results[4] == '0'  # mac2 out of second window
        assert results[5] == '1'  # mac1 out of second window
 
 
#Busy
"""Busy events zijn niet vaak vereist en moeten gemiddelden over een minuut zijn.
Met een facecount of soundcount = 0  moet nog steeds een busy signaal mogelijk zijn.

avg(3*fc+1)*(1+Nsg1)*(1+Nsg2) > threshold (to be measured)
Een wortel of logaritme van het geheel heeft geen invloed;
eventueel kun je de facecounts relatief belangrijker maken (kwadraat).
"""

class testQueryBusy(object):
    
    def setup(self):   # Run independently for every testcase
        self.cep = EsperEngine("TestBusy")
        self.cep.define_event('Busy', { 
            'avgfacecount': java.lang.Double,
            'nsg1': java.lang.Long,
            'nsg2': java.lang.Long,
            'busylevel': java.lang.Double
            })
        self.cep.define_event('AvgFacecount', { 
            'facecount': java.lang.Float,
            'avgfacecount': java.lang.Double
            })
        self.cep.define_event('CountSounds', { 
            'mac': java.lang.String,
            'nsg': java.lang.Long 
            })
        self.mocklisten = Mock()
        self.qman = QueryManager(self.cep)
        qa = queries.QueryBusy(100)
        self.qman.addQuery(qa.getQueries(), self.mocklisten)

    def testBusy(self):
        #Test Busy (met 1,1,1 en 3,49,99)
        self.cep.send_event({
            'facecount': 4.,
            'avgfacecount': 1.}, 'AvgFacecount')
        self.cep.send_event({
            'mac': 'mac1',
            'nsg': 1}, 'CountSounds')
        self.cep.send_event({
            'mac': 'mac2',
            'nsg': 1}, 'CountSounds')
        time.sleep(4.5)
        self.cep.send_event({
            'facecount': 4.,
            'avgfacecount': 3.}, 'AvgFacecount')
        self.cep.send_event({
            'mac': 'mac1',
            'nsg': 49}, 'CountSounds')
        self.cep.send_event({
            'mac': 'mac2',
            'nsg': 99}, 'CountSounds')
        time.sleep(0.5)
        print self.mocklisten.mock_calls
        results = re.findall("busylevel': (.*?)}", 
                          str(self.mocklisten.mock_calls))
        assert results[0] == '50000.0'


#!/usr/bin/env jython

# SenSafety.MidTerm.CEPengine provides the Esper based complex event processing
# engine for the mid-term SenSafety demo. 
# Main.py registers the query lists defined in this module.
# Query lists are returned by functions that accept configurable parameters.

# Marc de Lignie, Politie IV-organisatie
# September 24, 2014

import java.lang
import urllib, urllib2


ANOMALOUS_SOUND = 'Anomalous_Sound'  #ToDo: use in query
SOUNDGROUP = 'SoundGroup'            #ToDo: use in query
COUNTSOUNDS = 'CountSounds'          #ToDo: use in query
FACECOUNT = 'Facecount'
BUSY = 'Busy'
TILT = 'Tilt'
CONTACT = 'Contact'

# WebMonitor URLs
URL_SOUND = 'http://localhost:8555/SenSafety_MidTerm/eventdb/sound'
URL_FACE = 'http://localhost:8555/SenSafety_MidTerm/eventdb/face'
URL_TILT = 'http://localhost:8555/SenSafety_MidTerm/eventdb/tilt'
URL_BUSY = 'http://localhost:8555/SenSafety_MidTerm/eventdb/busy'
URL_SILENT = 'http://localhost:8555/SenSafety_MidTerm/eventdb/silent'


class QueryFacecount(object):

    def __init__(self, twindow):
        self.twindow = twindow

    def getResultEvent(self):
        return (FACECOUNT, { 
            'timestamp': java.lang.String, # ISO 8601
            'mac': java.lang.String,
            'facecount': java.lang.Float 
            })      

    def getQueries(self):
        #return ['select * from %s' % FACECOUNT]
        return [' '.join(['insert into AvgFacecount',
                'select avg(facecount) as avgfacecount',
                'from %s.win:time_batch(%i sec)'%(FACECOUNT,self.twindow)]
                )]

    def listener(self, data_new, data_old):
        if not isinstance(data_new, list):
            data_new = [data_new]
        for item in data_new:
            print 'Facecount event passed through CEPengine:\n', \
                  str(item)[:160]
            # Post to Web monitor (correct timestamp bug in facecount agent)
            event = {
                'mac': item['cam'],
                'timestamp': time.strftime("%Y-%m-%dT%H:%M:%S", 
                                  time.localtime(time.time())),
                'soundlevel': item['soundlevel']
                }
            urllib2.urlopen(URL_FACE, urllib.urlencode(event))


class QueryAnomalousSound(object):

    def getResultEvent(self):
        return (SOUNDGROUP, { 
            'timestamp': java.lang.String,
            'mac': java.lang.String,
            'soundlevel': java.lang.String 
            })      

    def getQueries(self):
        return [
            'insert into SoundGroup\
             select s1.timestamp as timestamp, s1.mac as mac,\
                 s1.soundlevel as soundlevel\
             from pattern[every s1=Anomalous_Sound() ->\
                 timer:interval(2 sec) and not s2=Anomalous_Sound(s1.mac=s2.mac)]'
               ]

    def listener(self, data_new, data_old):
        if not isinstance(data_new, list):
            data_new = [data_new]
        for item in data_new:
            print 'Anomalous sound event passed through CEPengine:\n', \
                  str(item)[:160]
            # Post to Web monitor
            urllib2.urlopen(URL_SOUND, urllib.urlencode(item))


class QueryCountSounds(object):

    def __init__(self, twindow):
        self.twindow = twindow

    def getResultEvent(self):
        return (COUNTSOUNDS, { 
            'mac': java.lang.String,
            'nsg': java.lang.Long }
            )    

    def getQueries(self):
        return [' '.join(['insert into CountSounds',
             'select mac, count(soundlevel) as nsg',
             'from SoundGroup.win:time_batch(%i sec)'% self.twindow,
             'group by mac'])
             ]
              
    def listener(self, data_new, data_old):
        if not isinstance(data_new, list):
            data_new = [data_new]
        for item in data_new:
            print 'CountSounds event passed through CEPengine:\n', \
                  str(item)[:160]


class QueryBusy(object):
    # Query is specifiek voor twee sound sensors en 1 facecount sensor.
    # AvgFacecount and CountSounds are almost synchronous
    #
    # It should be possible to simplify the pattern by replacing "->"
    # with "and" + using a different time window control,
    # but I am in a hurry now 

    def __init__(self, level):
        self.level = level

    def getResultEvent(self):
        return (BUSY, {
            'timestamp': java.lang.String, # ISO 8601
            'avgfacecount': java.lang.Double,
            'nsg1': java.lang.Long,
            'nsg2': java.lang.Long,
            'busylevel': java.lang.Double
            })

    def getQueries(self):
        return [' '.join(['insert into Busy',
           'select a.avgfacecount as avgfacecount,', 
             'cs1.nsg as nsg1, cs2.nsg as nsg2,',
             '(3*a.avgfacecount+1)*(1+cs1.nsg)*(1+cs2.nsg) as busylevel',
           'from pattern[(every a=AvgFacecount ->',
             'cs1=CountSounds where timer:within(4 sec)->',
             'cs2=CountSounds(cs1.mac!=cs2.mac) where timer:within(4 sec))',
             'or (every cs1=CountSounds ->',
             'a=AvgFacecount where timer:within(4 sec)->',
             'cs2=CountSounds(cs1.mac!=cs2.mac) where timer:within(4 sec))',
             'or (every cs1=CountSounds ->',
             'cs2=CountSounds(cs1.mac!=cs2.mac) where timer:within(4 sec) ->',
             'a=AvgFacecount where timer:within(4 sec))]',
           'where (3*a.avgfacecount+1)*(1+cs1.nsg)*(1+cs2.nsg) > %i'%self.level
           ])
           ]
              
    def listener(self, data_new, data_old):
        if not isinstance(data_new, list):
            data_new = [data_new]
        for item in data_new:
            print 'Busy event passed through CEPengine:\n', \
                  str(item)[:160]
            # Post to Web monitor
            eventdata = {
                'location': item['location'],
                'timestamp': item['timestamp'],
                'facecount': item['facecount'],
                'soundlevel': item['sound']}
            eventurl = URL_BUSY + urllib.urlencode(eventdata)
            urllib2.urlopen(eventurl)


class QueryTilt(object):

    def getQueries(self):
        return ['select * from %s' % TILT]

    def listener(self, data_new, data_old):
        if not isinstance(data_new, list):
            data_new = [data_new]
        for item in data_new:
            print 'Tilt event passed through CEPengine:\n', str(item)[:320]
            # Post to Web monitor
            eventdata = {
                'sensor_id': item['sensor_id'],
                'timestamp': item['timestamp'],
                'event': item['event'],
                'state': item['state']}
            if item['event'] == 'MOTIONSTART': 
                urllib2.urlopen(URL_TILT, urllib.urlencode(eventdata))
  
            
""" Not for MidTerm event
class QueryContact(object):
    # For now: just print incoming events after passing through the cep engine

    def getQueries(self):
        return ['select * from %s' % CONTACT]

    def listener(self, data_new, data_old):
        if not isinstance(data_new, list):
            data_new = [data_new]
        for item in data_new:
            print 'Contact event passed through CEPengine:\n', str(item)[:320]
"""



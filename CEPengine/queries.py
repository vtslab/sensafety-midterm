#!/usr/bin/env jython

# SenSafety.MidTerm.CEPengine provides the Esper based complex event processing
# engine for the mid-term SenSafety demo. 
# Main.py registers the query lists defined in this module.
# Query lists are returned by functions that accept configurable parameters.

# Marc de Lignie, Politie IV-organisatie
# March 26, 2014


def queryExample(example):
    # Example
    
    queries = [     
        'create variant schema anyEvent as *',
        'insert into anyEvent select * \
            from wifiPoll(message = "ASSOC")',
        'insert into anyEvent select * \
            from videoStill',
        'insert into anyTimeOrdered select * from anyEvent \
            output %s order by millisec' % example,
        'insert into wifiPollTimeOrdered select \
                cast(name, java.lang.String) as name,\
                cast(ap, java.lang.String) as ap, \
                cast(ddate, java.lang.String) as ddate, \
                cast(ttime, java.lang.String) as ttime, \
                cast(millisec, java.lang.Long) as millisec, \
                cast(mac, java.lang.String) as mac, \
                cast(message, java.lang.String) as message \
            from anyTimeOrdered(name = "wifiPoll")',
        'insert into videoStillTimeOrdered select \
                cast(name, java.lang.String) as name,\
                cast(cam, java.lang.String) as cam, \
                cast(ddate, java.lang.String) as ddate, \
                cast(ttime, java.lang.String) as ttime, \
                cast(millisec, java.lang.Long) as millisec, \
                cast(foto, java.lang.String) as foto \
            from anyTimeOrdered(name = "videoStill")']
    return queries


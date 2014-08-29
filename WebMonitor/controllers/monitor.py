# -*- coding: utf-8 -*-

"""
SenSafety.MidTerm.WebMonitor provides the web2py based web application for 
the mid-term SenSafety demo. It:
 - provides an overview page /SenSafety-MidTerm/ilp that shows the tilt events,
   silent events and busy events controlling the ILP's
 - provides a page with raw facecount events
 - provides a page with raw sound events
 
The web application is served by the web2py web server, started by init.d
on http://localhost:8555/

Marc de Lignie, Politie IV-organisatie, COMMIT/
August 29, 2014
"""

# Todo: push type Ajax using "Ajax long polling", see:
# http://en.wikipedia.org/wiki/Comet_%28programming%29
# Instead of periodic polling by the views.
# This will result in a more real-time response and less server load.

def ilp():
    # Displays tilt, silent and busy events, controlling the ILP's
    return dict()  # No input for view

def face():
    # Displays raw facecount events
    return dict()  # No input for view

def sound():
    # Displays raw sound events
    return dict()  # No input for view

def tiltevents():
    # https://datatables.net/release-datatables/examples/ajax/ajax.html
    events = []
    for row in db().select(db.tilt.ALL, orderby = ~db.tilt.eventtime, 
                           limitby = ( 0, 100)):
        events.append([row.sensor_id, row.eventtime, row.origin, row.status])
    return {'aaData': events}

def faceevents():
    # https://datatables.net/release-datatables/examples/ajax/ajax.html
    events = []
    for row in db().select(db.face.ALL, orderby = ~db.face.eventtime, 
                           limitby = ( 0, 100)):
        events.append([row.dataset, row.eventtime, row.facecount])
    return {'aaData': events}

def soundevents():
    # https://datatables.net/release-datatables/examples/ajax/ajax.html
    events = []
    for row in db().select(db.sound.ALL, orderby = ~db.sound.eventtime, 
                           limitby = ( 0, 100)):
        events.append([row.mac, row.eventtime, row.soundlevel])
    return {'aaData': events}

def silentevents():
    # https://datatables.net/release-datatables/examples/ajax/ajax.html
    events = []
    for row in db().select(db.silent.ALL, orderby = ~db.silent.eventtime, 
                           limitby = ( 0, 100)):
        events.append([row.place, row.eventtime, row.facecount, row.soundlevel])
    return {'aaData': events}

def busyevents():
    # https://datatables.net/release-datatables/examples/ajax/ajax.html
    events = []
    for row in db().select(db.busy.ALL, orderby = ~db.busy.eventtime, 
                           limitby = ( 0, 100)):
        events.append([row.place, row.eventtime, row.facecount, row.soundlevel])
    return {'aaData': events}



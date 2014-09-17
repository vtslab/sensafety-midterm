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
September 12, 2014
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

def timeline():
    import time
    timenow = time.time()
    soundevents = []
    for i in xrange(0, 20):
        event = {
            "id":"sound%i" % i,
            "title": "Test %i" % i,
            "description":"Test%i" % i,
            "startdate": time.strftime("%Y-%m-%d %H:%M:%S", 
                                  time.localtime(timenow - i * 300)),
            "enddate":"",
            "importance":"10",
            "date_display":"ho",
            "icon":"circle_green.png"
        }
        soundevents.append(event)
    faceevents = []
    for i in xrange(0, 20):
        event = {
            "id":"face%i" % i,
            "title": "Test %i" % i,
            "description":"Test%i" % i,
            "startdate": time.strftime("%Y-%m-%d %H:%M:%S", 
                                  time.localtime(timenow - i * 320)),
            "enddate":"",
            "importance":"10",
            "date_display":"ho",
            "icon":"circle_green.png"
        }
        faceevents.append(event)
    jsonhist = {
        "presentation":"Timeglider",
        "title":"All events",
        "description":"Hoi",
        "open_modal":True,
        "initial_zoom":3,
        "image_lane_height":100,
        "focus_date":time.strftime("%Y-%m-%d %H:%M:%S",
                              time.localtime(timenow - 1000)),
        "initial_timelines":["sound", "facecount"],
        "timelines":[{
            "focus_date":time.strftime("%Y-%m-%d %H:%M:%S",
                                  time.localtime(timenow - 1000)),
            "title":"Sound events",
            "description":"Sound events",
            "id":"sound",
            "initial_zoom":3,
            "bottom":"250",
            "events":soundevents
            },{
            "focus_date":time.strftime("%Y-%m-%d %H:%M:%S",
                                  time.localtime(timenow - 1000)),
            "title":"Face detection events",
            "id":"facecount",
            "description":"Face detection events",
            "initial_zoom":3,
            "bottom":"180",
            "inverted":True,
            "events":faceevents}]
        }
    return jsonhist
    
""" Example code for serving a png from matplotlib.
It appears you can also do plt.savefig(buf,format="png",facecolor="white") or fig.savefig(). So you dont have to deal with the canvas object.
    
import cStringIO
from matplotlib.figure import Figure                      
from matplotlib.backends.backend_agg import FigureCanvasAgg

fig = Figure(figsize=[4,4])                               
ax = fig.add_axes([.1,.1,.8,.8])                          
ax.scatter([1,2], [3,4])                                  
canvas = FigureCanvasAgg(fig)

# write image data to a string buffer and get the PNG image bytes
buf = cStringIO.StringIO()
canvas.print_png(buf)
data = buf.getvalue()

# pseudo-code for generating the http response from your
# webserver, and writing the bytes back to the browser.
# replace this with corresponding code for your web framework
headers = {
    'Content-Type': 'image/png',
    'Content-Length': len(data)
    }
response.write(200, 'OK', headers, data) """
    


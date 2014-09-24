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
September 19, 2014
"""
# Todo: push type Ajax using "Ajax long polling", see:
# http://en.wikipedia.org/wiki/Comet_%28programming%29
# Instead of periodic polling by the views.
# This will result in a more real-time response and less server load.

import cStringIO, time
from matplotlib import rcParams
import matplotlib.pyplot as plt
import numpy as np


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    session.forget()
    return service()

@service.run    
def ilp():
    # Displays tilt, silent and busy events, controlling the ILP's
    return dict()  # No input for view

@service.run
def face():
    # Displays raw facecount events
    return dict()  # No input for view

@service.run
def sound():
    # Displays raw sound events
    return dict()  # No input for view

@service.run
def tiltevents():
    # https://datatables.net/release-datatables/examples/ajax/ajax.html
    events = []
    for row in db().select(db.tilt.ALL, orderby = ~db.tilt.eventtime, 
                           limitby = ( 0, 100)):
        events.append([row.sensor_id, row.eventtime, row.origin, row.status])
    return {'aaData': events}

@service.run
def faceevents():
    # https://datatables.net/release-datatables/examples/ajax/ajax.html
    events = []
    for row in db().select(db.face.ALL, orderby = ~db.face.eventtime, 
                           limitby = ( 0, 100)):
        events.append([row.dataset, row.eventtime, row.facecount])
    return {'aaData': events}

@service.run
def soundevents():
    # https://datatables.net/release-datatables/examples/ajax/ajax.html
    events = []
    for row in db().select(db.sound.ALL, orderby = ~db.sound.eventtime, 
                           limitby = ( 0, 100)):
        events.append([row.mac, row.eventtime, row.soundlevel])
    return {'aaData': events}

@service.run
def silentevents():
    # https://datatables.net/release-datatables/examples/ajax/ajax.html
    events = []
    for row in db().select(db.silent.ALL, orderby = ~db.silent.eventtime, 
                           limitby = ( 0, 100)):
        events.append([row.place, row.eventtime, row.facecount, row.soundlevel])
    return {'aaData': events}

@service.run
def busyevents():
    # https://datatables.net/release-datatables/examples/ajax/ajax.html
    events = []
    for row in db().select(db.busy.ALL, orderby = ~db.busy.eventtime, 
                           limitby = ( 0, 100)):
        events.append([row.place, row.eventtime, row.facecount, row.soundlevel])
    return {'aaData': events}




""" Example eventplot with offsets and varibale linewidths
def timeline():
    matplotlib.rcParams['font.size'] = 8.0

    # set the random seed
    np.random.seed(0)

    # create random data
    data1 = np.random.random([6, 20])

    # set different colors for each set of positions
    colors1 = np.array([[1, 0, 0],
                        [0, 1, 0],
                        [0, 0, 1],
                        [1, 1, 0],
                        [1, 0, 1],
                        [0, 1, 1]])

    # set different line properties for each set of positions
    # note that some overlap
    lineoffsets1 = np.array([-15, -3, 1, 1.5, 6, 10])
    linelengths1 = [5, 2, 1, 1, 3, 1.5]
    linewidths1 = [[1,2,3,4,5,1,2,3,4,5,1,2,3,4,5,1,2,3,4,5],2,3,4,5,6]

    fig = plt.figure()

    # create a horizontal plot
    ax1 = fig.add_subplot(221)
    ax1.eventplot(data1, colors=colors1, lineoffsets=lineoffsets1,
                  linelengths=linelengths1, linewidths=linewidths1)


    # create a vertical plot
    ax2 = fig.add_subplot(223)
    ax2.eventplot(data1, colors=colors1, lineoffsets=lineoffsets1,
                  linelengths=linelengths1, orientation='vertical')

    # create another set of random data.
    # the gamma distribution is only used fo aesthetic purposes
    data2 = np.random.gamma(4, size=[60, 50])

    # use individual values for the parameters this time
    # these values will be used for all data sets (except lineoffsets2, which
    # sets the increment between each data set in this usage)
    colors2 = [[0, 0, 0]]
    lineoffsets2 = 1
    linelengths2 = 1

    # create a horizontal plot
    ax1 = fig.add_subplot(222)
    ax1.eventplot(data2, colors=colors2, lineoffsets=lineoffsets2,
                  linelengths=linelengths2)


    # create a vertical plot
    ax2 = fig.add_subplot(224)
    ax2.eventplot(data2, colors=colors2, lineoffsets=lineoffsets2,
                  linelengths=linelengths2, orientation='vertical')
    buf = cStringIO.StringIO()
    plt.savefig(buf, format="png" ,facecolor="white")
    data = buf.getvalue()
    return data"""


@service.run
def timeline():
    todaydate = time.strftime("%Y-%m-%dT", time.localtime(time.time()))
    tilt = []
    for row in db().select(db.tilt.eventtime):
        if row.eventtime[0:10] == todaydate:
            tilt.append(row.eventtime)
    silent = []
    for row in db().select(db.silent.eventtime):
        if row.eventtime[0:10] == todaydate:
            silent.append(row.eventtime)
    busy = []
    for row in db().select(db.busy.eventtime):
        if row.eventtime[0:10] == todaydate:
            busy.append(row.eventtime)
    sound2 = []
    sound1 = []
    for row in db().select(db.sound.eventtime):
        if row.eventtime[0:10] == todaydate:
            sound2.append(row.eventtime)
            sound1.append(row.eventtime)
    face = []
    for row in db().select(db.face.eventtime):
        if row.eventtime[0:10] == todaydate:
            face.append(row.eventtime)
    data = [tilt, silent, busy, sound2, sound1, face]
    """
    np.random.seed(int(time.time()))
    data = [100. + 0.4*np.random.random(10),100. + 0.4*np.random.random(40),100. + 0.4*np.random.random(50),100. + 0.4*np.random.random(50),100. + 0.4*np.random.random(50),100. + 0.4*np.random.random(50)]"""
    colors = [[0, 0, 0],[0, 1, 0],[0, 0, 0],[0, 0, 1],[0, 0, 1],[0, 0, 0]]
    streamlabels = ['','Tilt', 'Silent', 'Busy','Sound anomaly','Sound anomaly','Face count']
    rcParams['font.size'] = 8.0

    #matplotParams['font.size'] = 12.0
    fig, ax = plt.subplots(figsize=(15,5))
    #ax = fig.add_subplot()
    # Facecount plot
    ylabels = ['' for i in xrange(len(ax.get_yticklabels()))]
    ax.set_yticklabels(streamlabels)
    ax.xaxis_date()
    ax.eventplot(data, colors=colors, label=streamlabels) 
    # Soundlevel plots for smartphones 1 and 2
    # Busy events plot
    # Silent events plot
    # Tilt events plot

    # write image data to a string buffer and get the PNG image bytes
    buf = cStringIO.StringIO()
    #plt.tight_layout.auto_adjust_subplotpars(subplot_list=np.array([ax1,ax2]), w_pad=0)
    plt.savefig(buf, format="png" ,facecolor="white")
    data = buf.getvalue()
    plt.close('all')
    return data




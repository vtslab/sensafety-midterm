# -*- coding: utf-8 -*-

# Todo: cron job for removing old database records


def tilt():  # Accept and store tilt events
    pv = request.post_vars
    #print str(pv)
    db.tilt.insert(**{
        'sensor_id': pv.sensor_id,
        'eventtime': pv.timestamp,
        'origin': pv.event,
        'status': pv.state})
    return str(pv)  # Echo posted parameters


def face():  # Accept and store facecount events
    pv = request.post_vars
    #print str(pv)
    db.face.insert(**{
        'mac': pv.mac,
        'eventtime': pv.timestamp,
        'facecount': pv.facecount})
    return str(pv)  # Echo posted parameters


def sound():  # Accept and store sound events
    pv = request.post_vars
    #print str(pv)
    db.sound.insert(**{
        'mac': pv.mac,
        'eventtime': pv.timestamp,
        'soundlevel': pv.soundlevel})
    return str(pv)  # Echo posted parameters


def activity():  # Accept and store activity events
    pv = request.post_vars
    #print str(pv)
    db.activity.insert(**{
        'eventtime': pv.timestamp,
        'eventtype': pv.eventtype,
        'busylevel': pv.busylevel,
        'facecount': pv.facecount,
        'soundlevel': pv.soundlevel})
    return str(pv)  # Echo posted parameters



# -*- coding: utf-8 -*-

# Todo: cron job for removing old database records


def tilt():  # Accept and store tilt events
    pv = request.post_vars
    db.tilt.insert(**{
        'sensor_id': pv.sensor_id,
        'eventtime': pv.timestamp,
        'origin': pv.event,
        'status': pv.state})
    return str(pv)  # Echo posted parameters


def face():  # Accept and store facecount events
    pv = request.post_vars
    db.face.insert(**{
        'mac': pv.mac,
        'eventtime': pv.timestamp,
        'facecount': pv.facecount})
    return str(pv)  # Echo posted parameters


def sound():  # Accept and store sound events
    pv = request.post_vars
    print str(pv)
    db.sound.insert(**{
        'mac': pv.mac,
        'eventtime': pv.timestamp,
        'soundlevel': pv.soundlevel})
    return str(pv)  # Echo posted parameters


def silent():  # Accept and store silent events
    pv = request.post_vars
    db.silent.insert(**{
        'place': pv.location,
        'eventtime': pv.timestamp,
        'facecount': pv.facecount,
        'soundlevel': pv.soundlevel})
    return str(pv)  # Echo posted parameters


def busy():  # Accept and store busy events
    pv = request.post_vars
    print pv
    db.busy.insert(**{
        'place': pv.location,
        'eventtime': pv.timestamp,
        'facecount': pv.facecount,
        'soundlevel': pv.soundlevel})
    return str(pv)  # Echo posted parameters



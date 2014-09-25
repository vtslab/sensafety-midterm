#!/usr/bin/env jython

# SenSafety.MidTerm.CEPengine provides the Esper based complex event processing
# engine for the mid-term SenSafety demo. 
# The module ilpcontrolstandalone allows to control the ILP's without the
# CEPengine

# Marc de Lignie, Politie IV-organisatie, COMMIT/
# Sept 25, 2014

import time
from main import MQTT_BROKER_LOCAL
import paho, ilpcontrol

BUSYTIMEOUT = 4

if __name__ == "__main__":
    pahoclient_local = paho.PahoClient(MQTT_BROKER_LOCAL)    
    ilpclient = ilpcontrol.ILPControl(pahoclient_local, 
                                      BUSYTIMEOUT, nosilent=True)
    time.sleep(0.3)
    print "Tilt event"
    ilpclient.tilt()
    time.sleep(2)
    print "Silent event"
    ilpclient.silent(override=True)
    time.sleep(2)
    print "Five Busy events"
    ilpclient.busy()
    ilpclient.busy()
    ilpclient.busy()
    ilpclient.busy()
    ilpclient.busy()
    while True:   # Do nothing until CTRL+C keyboard interrupt
        time.sleep(3000)
    time.sleep(0.5)
    ilpclient.stop
    pahoclient_local.close()

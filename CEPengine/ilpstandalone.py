#!/usr/bin/env jython

# SenSafety.MidTerm.CEPengine provides the Esper based complex event processing
# engine for the mid-term SenSafety demo. 
# The module ilpcontrolstandalone allows to control the ILP's without the
# CEPengine

# Marc de Lignie, Politie IV-organisatie, COMMIT/
# Sept 25, 2014

import time
from main import MQTT_BROKER_LOCAL, MAXBUSY, MINQUIET
import paho, ilpcontrol

if __name__ == "__main__":
    pahoclient_local = paho.PahoClient(MQTT_BROKER_LOCAL)    
    ilpclient = ilpcontrol.ILPControl(pahoclient_local, MAXBUSY, MINQUIET)
    time.sleep(0.3)
    print "Tilt event"
    ilpclient.tilt()
    time.sleep(5)
    print "Silent event"
    ilpclient.silent()
    time.sleep(5)
    print "Five Busy events"
    ilpclient.busy(True)
    ilpclient.busy(True)
    ilpclient.busy(True)
    ilpclient.busy(True)
    ilpclient.busy(True)
    time.sleep(5)
    print "Ten Silent events"
    ilpclient.busy(False)
    ilpclient.busy(False)
    ilpclient.busy(False)
    ilpclient.busy(False)
    ilpclient.busy(False)
    ilpclient.busy(False)
    ilpclient.busy(False)
    ilpclient.busy(False)
    ilpclient.busy(False)
    ilpclient.busy(False)
    while True:   # Do nothing until CTRL+C keyboard interrupt
        ilpclient.tilt()
        time.sleep(10)
    time.sleep(0.5)
    ilpclient.stop
    pahoclient_local.close()

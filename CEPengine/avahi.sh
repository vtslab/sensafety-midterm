#!/bin/sh

ESPER_LOCATION=/home/m-doit/Python/Esper/esper-4.9.0
CLASSPATH=$ESPER_LOCATION/esper/lib/antlr-runtime-3.2.jar:$CLASSPATH
CLASSPATH=$ESPER_LOCATION/esper/lib/cglib-nodep-2.2.jar:$CLASSPATH
CLASSPATH=$ESPER_LOCATION/esper/lib/commons-logging-1.1.1.jar:$CLASSPATH
CLASSPATH=$ESPER_LOCATION/esper/lib/log4j-1.2.16.jar:$CLASSPATH
CLASSPATH=$ESPER_LOCATION/esper-4.9.0.jar:$CLASSPATH
CLASSPATH=/home/m-doit/Python/SenSafety/avahi4j-0.1/avahi4j.jar:$CLASSPATH
export CLASSPATH

/usr/bin/jython avahi.py

exit 0

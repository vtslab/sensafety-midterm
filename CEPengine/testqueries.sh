#!/bin/sh

ESPER_LOCATION=/home/m-doit/Python/Esper/esper-4.9.0
CLASSPATH=$ESPER_LOCATION/esper/lib/antlr-runtime-3.2.jar:$CLASSPATH
CLASSPATH=$ESPER_LOCATION/esper/lib/cglib-nodep-2.2.jar:$CLASSPATH
CLASSPATH=$ESPER_LOCATION/esper/lib/commons-logging-1.1.1.jar:$CLASSPATH
CLASSPATH=$ESPER_LOCATION/esper/lib/log4j-1.2.16.jar:$CLASSPATH
CLASSPATH=$ESPER_LOCATION/esperio-http-4.9.0.jar:$CLASSPATH
CLASSPATH=$ESPER_LOCATION/esper-4.9.0.jar:$CLASSPATH
export CLASSPATH

/usr/lib/jython2.5.3/bin/nosetests --nocapture testqueries.py

exit 0

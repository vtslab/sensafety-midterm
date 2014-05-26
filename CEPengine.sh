#!/bin/sh

#ESPER_LOCATION=../esper-4.9.0
#CLASSPATH=$ESPER_LOCATION/esper-4.9.0.jar:$CLASSPATH
#CLASSPATH=$ESPER_LOCATION/esper/lib/*:$CLASSPATH
#CLASSPATH=$ESPER_LOCATION/esperio-http-4.9.0.jar:$CLASSPATH
#CLASSPATH=$ESPER_LOCATION/esperio-http/lib/*:$CLASSPATH
#CLASSPATH=../avahi4j-0.1/avahi4j.jar:$CLASSPATH
CLASSPATH=lib/*:$CLASSPATH
export CLASSPATH

java -Dpython.cachedir.skip=false -Dpython.cachedir=/tmp \
     -Djava.library.path=lib \
    org.python.util.jython CEPengine/main.py

exit 0

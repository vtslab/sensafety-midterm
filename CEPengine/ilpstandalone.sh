#!/bin/sh

CLASSPATH=../lib/*:$CLASSPATH
CLASSPATH="../../Noldus-NCF-0.10/NCF/0.10/Java/Lib/Noldus Communication Framework.jar":$CLASSPATH
export CLASSPATH

java -Dpython.cachedir.skip=false -Dpython.cachedir=/tmp \
    org.python.util.jython ilpstandalone.py

exit 0

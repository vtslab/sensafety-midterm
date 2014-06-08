#!/bin/sh

CLASSPATH=../lib/*:$CLASSPATH
export CLASSPATH

java -Dpython.cachedir.skip=false -Dpython.cachedir=/tmp \
    org.python.util.jython paho.py

exit 0

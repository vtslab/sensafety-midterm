#!/bin/sh

CLASSPATH=../lib/*:$CLASSPATH
export CLASSPATH

jython paho.py

exit 0

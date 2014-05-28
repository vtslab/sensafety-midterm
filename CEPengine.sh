#!/bin/sh

CLASSPATH=lib/*:$CLASSPATH
export CLASSPATH

arch=`uname -m`
if [ $arch == "x86_64" ]; then
    libpath=lib/x86_64
else
    libpath=lib/i386
fi

java -Dpython.cachedir.skip=false -Dpython.cachedir=/tmp \
     -Djava.library.path=$libpath \
    org.python.util.jython CEPengine/main.py

exit 0

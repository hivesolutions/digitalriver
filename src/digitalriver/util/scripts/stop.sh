#!/bin/sh

for directory in /torus/features/* ; do
    if [ -d $directory ]; then
        if [ -e $directory/stop.sh ]; then
            $directory/stop.sh
        fi
    fi
done

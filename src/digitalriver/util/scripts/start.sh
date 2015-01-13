#!/bin/sh

for directory in /torus/features/* ; do
    if [ -d $directory ]; then
        if [ -e $directory/start.sh ]; then
            $directory/start.sh
        fi
    fi
done

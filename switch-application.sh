#!/bin/sh
xdotool keydown alt
sleep .1

xdotool keydown Tab
sleep .1
xdotool keyup Tab

sleep .05
xdotool key Left
sleep .3

for (( i = 0; i < "$2"; i++ ))
do
    xdotool key "$1"
    sleep .15

    if [ "$i" == 0 ] && [ "$1" == "Left" ]; then
        sleep .2
    fi
done

xdotool keyup alt

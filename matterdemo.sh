#! /bin/sh
export NWIFACE="$(snapctl get nwiface)"
export DEBUG="$(snapctl get debug)"
export FORWARDEDIP="$(snapctl get forwardedip)"

$SNAP/bin/python3 $SNAP/thirdapp.py
#python3.10 $SNAP/thirdapp.py

#! /bin/sh
export DEBUG="$(snapctl get debug)"
export NWIFACE="$(snapctl get nwiface)"
export FORWARDEDIP="$(snapctl get forwardedip)"

$SNAP/bin/python3 $SNAP/firstapp.py
#python3.10 $SNAP/firstapp.py

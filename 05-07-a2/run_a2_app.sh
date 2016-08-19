#!/usr/bin/env sh
cd /home/pi/toku1/05-07-a2
. ../python3-toku1/bin/activate
python3 app_a2.py $@ &
deactivate
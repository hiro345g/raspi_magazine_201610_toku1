#!/usr/bin/env sh
cd /home/pi/toku1/12-15-a4
python3 datalogger_weather_stop.py
sleep 5
python3 datacheck_weather.py
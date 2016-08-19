#!/usr/bin/env sh
cd /home/pi/toku1/12-15-a4
pid=`pgrep -f "python3 datalogger_weather.py"`
if [ $? -eq 0 ]; then
    echo "datalogger_weather.py is running"
else
    python3 datalogger_weather.py &
fi
FLASK_DEBUG=1 FLASK_APP=server_12_datalogger_weather.py flask run -h 0.0.0.0

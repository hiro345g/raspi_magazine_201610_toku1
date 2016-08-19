#!/usr/bin/env sh
APP_DIR="/home/pi/toku1/12-15-a4"
cd ${APP_DIR}
pid=`pgrep -f "python3 datalogger_weather.py"`
if [ $? -eq 0 ]; then
    echo "datalogger_weather.py is running"
else
    python3 datalogger_weather.py &
fi

pid=`pgrep -f "python3 graph_generater_wheather.py"`
if [ $? -eq 0 ]; then
    echo "graph_generater_wheather.py is running"
else
    cd ${APP_DIR};
    DISPLAY=:0 python3 graph_generater_wheather.py &
fi

pid=`pgrep -f "python3 app_a4.py"`
if [ $? -eq 0 ]; then
    echo "app_a4.py is running"
else
    cd ${APP_DIR};
    python3 app_a4.py &
fi

python3 server_a4.py

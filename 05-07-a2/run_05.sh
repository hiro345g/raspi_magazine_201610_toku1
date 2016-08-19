#!/usr/bin/env sh
cd /home/pi/toku1/05-07-a2
. ../python3-toku1/bin/activate
pid=`pgrep -f "python app_05.py"`
if [ $? -eq 0 ]; then
    echo "app_05.py is running"
else
    python app_05.py &
fi
python server_05.py

deactivate

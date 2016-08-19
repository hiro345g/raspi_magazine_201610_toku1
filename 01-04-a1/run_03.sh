#!/usr/bin/env bash
cd /home/pi/toku1/01-04-a1
. ../python3-toku1/bin/activate
if [ -e /home/pi/toku1/01-04-a1/app_03.db ];then
  rm /home/pi/toku1/01-04-a1/app_03.db
fi
python app_03.py &
python server_03.py
deactivate
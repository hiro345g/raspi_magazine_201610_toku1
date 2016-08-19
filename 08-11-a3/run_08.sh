#!/usr/bin/env sh
if [ -e /var/ramdisk/08-11-a3 ]; then
  rm -fr /var/ramdisk/08-11-a3
fi
cp -r /home/pi/toku1/08-11-a3 /var/ramdisk/
cd /var/ramdisk/08-11-a3
DISPLAY=:0 python3 server_08.py

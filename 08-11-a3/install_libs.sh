#!/usr/bin/env sh
DIR_LIB=${HOME}/toku1/08-11-a3/static/libs
if [ ! -e "${DIR_LIB}/js" ]; then
  mkdir -p "${DIR_LIB}/js"
fi

wget -O "${DIR_LIB}/js/jquery-3.1.0.min.js" https://code.jquery.com/jquery-3.1.0.min.js
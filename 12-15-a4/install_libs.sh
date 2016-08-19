#!/usr/bin/env sh
BASE_DIR=${HOME}/toku1/12-15-a4

# JavaScript用ディレクトリのチェック。ない場合ば作成
DIR_LIB=${BASE_DIR}/static/libs
if [ ! -e "${DIR_LIB}/js" ]; then
  mkdir -p "${DIR_LIB}/js"
fi

# wgetコマンドによる jQueryのダウンロード
wget -O "${DIR_LIB}/js/jquery-3.1.0.min.js" https://code.jquery.com/jquery-3.1.0.min.js

# apt-get による raspbianパッケージのインストール
sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get -y install i2c-tools python3-smbus sqlite3 python3-seaborn

# pip3 による Python3用モジュールのインストール
sudo pip3 install -r ${BASE_DIR}/requirements.txt

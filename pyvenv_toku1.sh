#!/bin/sh
BASE_DIR="${HOME}"/toku1

# 特集用ディレクトリー toku1/ の作成
if [ ! -e ${BASE_DIR} ]; then
  mkdir ${BASE_DIR}
fi

# python3-venvインストール
sudo apt-get update && sudo apt-get -y upgrade
sudo apt-get -y install python3-venv

# カレントをtoku1/にしてpython3-toku1を用意
cd ${BASE_DIR}
pyvenv python3-toku1

# 必要なモジュール一覧を記載した
# requirements.txt の作成
cat << EOF > requirements.txt
flask
wiringpi
EOF

# python3-toku1を有効化して必要なモジュールをインストール
. python3-toku1/bin/activate
pip install wheel
pip install -r requirements.txt

# python3-toku1の無効化
deactivate

#!/usr/bin/env sh
BASE_DIR="${HOME}/toku1/12-15-a4"
if [ ! -e ${BASE_DIR} ]; then
  mkdir -p ${BASE_DIR}
fi

# データベース名の指定
# SQLIte3ではCREATE DATABASEをしなくても
# 後のCREATE TABLEのときに自動で指定した
# ${DB_NAME}のデータベースがファイルで作成される
DB_NAME="${BASE_DIR}/bme280_sqlite3.db"

# データベース・テーブル作成
# CREATE TABLE テーブル名 ( カラム定義リスト PRIMARY KEY(カラム名))
# カラム定義リストは、「カラム名 カラム制約」を「,」で区切ったリスト
# ＊ NOT NULLは必須の意味
# ＊ DEFAULT CURRENT_TIMESTAMPは現在時刻を初期値にすること
# ＊ PRIMARY KEYでデータを検索するときの主キーとなるカラムを指定
for table_name in air_pressure humidity temperature
do
  echo "データベース・テーブル作成 ${DB_NAME}.${table_name}"
  SQL="CREATE TABLE ${table_name} ( \
    id INTEGER NOT NULL, \
    created_datetime DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL, \
    value FLOAT NOT NULL, \
    PRIMARY KEY (id) \
  );"
  echo ${SQL} | sqlite3 ${DB_NAME}
done

# サンプルデータ作成
# INSERT INTO テーブル名 (カラム名リスト) VALUES (値リスト)
# カラム名リストは、カラム名を「,」で区切ったリスト
# 値リストは、カラム名リストに対応する値を「,」で区切ったリスト
for table_name in air_pressure humidity temperature
do
  for v in 1 2 3 4
  do
    echo "サンプルデータ作成 ${table_name} 0.${v}"
    SQL="INSERT INTO ${table_name} (value) VALUES (0.${v});"
    echo ${SQL} | sqlite3 ${DB_NAME};
    sleep 1;
  done
done

# なお、サンプルデータを削除するには、次のコマンドを実行します。
#  * $ はプロンプトです。
# $ sh ~/toku1/12-15-a4/delete_sample_sqlite3_database.sh

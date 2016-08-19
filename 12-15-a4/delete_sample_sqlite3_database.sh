#!/usr/bin/env sh
BASE_DIR="${HOME}/toku1/12-15-a4"
if [ ! -e ${BASE_DIR} ]; then
  mkdir -p ${BASE_DIR}
fi

# データベース名の指定
DB_NAME="${BASE_DIR}/bme280_sqlite3.db"

# サンプルデータ削除
for table_name in air_pressure humidity temperature
do
  for v in 1 2 3 4
  do
    echo "サンプルデータ削除 ${table_name} 0.${v}"
    SQL="DELETE FROM ${table_name} WHERE id=${v} AND value=0.${v};"
    echo ${SQL} | sqlite3 ${DB_NAME}
  done
done

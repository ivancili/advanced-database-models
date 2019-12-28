#!/usr/bin/env bash

import_json_to_db() {

  json_file=$1

  mongoimport \
    -u $MONGO_INITDB_ROOT_USERNAME \
    -p $MONGO_INITDB_ROOT_PASSWORD \
    --authenticationDatabase admin \
    -d nmbp \
    -c $(basename -s .json $json_file) \
    --type json \
    --file $json_file
}

for file in $(find /docker-entrypoint-initdb.d/ -type f -name '*json'); do
  import_json_to_db $file
done

mongo \
  -u $MONGO_INITDB_ROOT_USERNAME \
  -p $MONGO_INITDB_ROOT_PASSWORD \
  --authenticationDatabase admin \
  --eval 'db.news.createIndex({date: -1})' \
  nmbp

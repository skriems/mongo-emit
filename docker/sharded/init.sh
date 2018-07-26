#!/bin/bash

echo "> init config replicaset"
mongo --port 27019 < ./scripts/init-cfgsvr.js
echo "> init shard1 replicaset"
mongo --port 27001 < ./scripts/init-sh1.js
echo "> init shard2 replicaset"
mongo --port 27002 < ./scripts/init-sh2.js

# sh1aMaster=`mongo --port 27001 -quiet --eval "db.isMaster().ismaster"`
# if [ "$sh1aMaster" == "true" ]; then
#     PRIME="sh1a"
#     PORT=27001
# else
#     PRIME="sh1b"
#     PORT=27003
# fi
# echo "> adding Arbiter sh1Arb on PRIMARY: $PRIME"
# mongo --port $PORT --eval "rs.addArb('sh1Arb:27005')"
# 
# sh2aMaster=`mongo --port 27002 -quiet --eval "db.isMaster().ismaster"`
# if [ "$sh2aMaster" == "true" ]; then
#     PRIME="sh2a"
#     PORT=27002
# else
#     PRIME="sh2b"
#     PORT=27004
# fi
# echo "> adding Arbiter sh2Arb on PRIMARY: $PRIME"
# mongo --port $PORT --eval "rs.addArb('sh2Arb:27006')"

echo "> MongoDemocracy: waiting 20sec for elections..."
sleep 20
mongo < ./scripts/init-router.js

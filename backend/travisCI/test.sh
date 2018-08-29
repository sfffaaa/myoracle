#!/bin/bash

set -e
cd backend

# start private chain
(cd travisCI; sh startnode1.sh &)
sleep 240

python3 testcase/oracle_wallet_test.py

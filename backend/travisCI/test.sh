#!/bin/bash

set -e
cd backend

# start private chain
(cd travisCI; sh startnode1.sh 2> /dev/null 1> /dev/null &)
sleep 20

pwd
python3 testcase/oracle_wallet_test.py

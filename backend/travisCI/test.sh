#!/bin/bash

set -e
cd backend

# start private chain
(cd travisCI; sh startnode1.sh &)

echo "==== Wait for Ethash finish first time ===="
sleep 240

echo "==== Running test case ===="
sh testcase/test_run.sh

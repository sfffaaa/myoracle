#!/bin/bash

set -e
cd backend

# start private chain
(cd travisCI; sh startnode1.sh &)
sleep 240

sh testcase/test_run.sh

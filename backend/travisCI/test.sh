#!/bin/bash

set -e
cd backend

ETHASH_PATH_EXIST=1

if [ ! -d "${HOME}/.ethash" ]; then
	ETHASH_PATH_EXIST=0
fi

# start private chain
(cd travisCI; sh startnode1.sh &)

if [ x"${ETHASH_PATH_EXIST}" == x"0" ]; then
	echo "==== Wait for Ethash finish first time ===="
	sleep 240
fi

echo "==== Running test case ===="
sh testcase/test_run.sh

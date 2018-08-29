#!/bin/bash

set -e

ganache-cli -p 9545 2> /dev/null 1> /dev/null &
cd solidity
sleep 15 # to make sure ganache-cli is up and running before compiling
rm -rf build
truffle compile
truffle migrate --reset --network development
truffle test
kill -9 $(lsof -t -i:9545)

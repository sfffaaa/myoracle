#!/bin/bash

set -e

geth --datadir "datadir" --keystore "keystore" init genesis.json
geth --identity "node1" --networkid 1994 --datadir "datadir" --keystore "keystore" --nodiscover --rpc --port "30303" --unlock "0,1,2,3,4" --password "password.sec" --mine --minerthreads=1

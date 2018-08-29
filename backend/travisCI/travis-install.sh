#!/bin/bash

set -e

cd backend

mkdir testcase/etc
cp travisCI/test_config.conf testcase/etc/test_config.conf
pip3 install -r requirements.txt

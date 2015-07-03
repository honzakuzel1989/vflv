#!/usr/bin/env bash

export VFLV_SERVER_PORT='2223'
export VFLV_SERVER_HOST=`ifconfig | awk '/inet addr/{print substr($2,6)}' | head -n 1`

cd /home/bananapi/vflv/LunchVoting
python2.7 runserver.py 1>OUT 2>ERR
cd -


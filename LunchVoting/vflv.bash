#!/usr/bin/env bash

export VFLV_SERVER_PORT='2223'
export VFLV_SERVER_HOST='192.168.2.62'

cd /home/ubuntu/Programs/flask/vflv/LunchVoting/
python2.7 runserver.py 1>OUT 2>ERR
cd -

#!/bin/sh

ps -ef | grep gearWork.py | grep -v grep | awk -F' '  '{ print $2 }' | xargs kill -9


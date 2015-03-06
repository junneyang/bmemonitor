#!/bin/sh

ps -ef | grep bmeMonitor.py | grep -v grep | awk -F' '  '{ print $2 }' | xargs kill -9


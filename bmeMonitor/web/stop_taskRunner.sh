#!/bin/sh

ps -ef | grep taskRunner.py | grep -v grep | awk -F' '  '{ print $2 }' | xargs kill -9


#!/bin/sh

pulseaudio --start -vvv --disallow-exit --log-target=syslog --high-priority --exit-idle-time=-1 --daemonize

exec "$@"
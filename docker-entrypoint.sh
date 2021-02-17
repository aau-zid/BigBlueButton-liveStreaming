#!/bin/bash

. /usr/src/app/nsswrapper.sh

if pulseaudio --check ; then
	echo "Pulseaudio already running - killing it..."
	pulseaudio --kill
fi

# sometimes pulseaudio fails to start (for unknown reason - try starting it again)
p=0

while ! pulseaudio --check && [ $p -lt 2 ] ; do
	echo "Starting pulseaudio..."
	pulseaudio --start -vvv --disallow-exit --log-target=syslog --high-priority --exit-idle-time=-1 &

	i=0

	while ! pulseaudio --check && [ $i -lt 3 ] ; do
		echo "Waiting for pulseaudio to start..."
		sleep 1
		i=$((i+1))
	done

	p=$((p+1))
done

if pulseaudio --check ; then
	exec "$@"
else
	echo "Error starting pulseaudio"
fi

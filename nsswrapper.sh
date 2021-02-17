#!/bin/sh

if test "`id -u`" -ne 0; then
    if test -s /tmp/pulse-passwd; then
	echo Skipping nsswrapper setup - already initialized
    else
	echo Setting up nsswrapper mapping `id -u` to lithium
	if test `id -g` -ne 0; then
	    sed "s|^lithium:.*|lithium:x:`id -g`:|" /etc/group >/tmp/pulse-group
	    sed \
		"s|^lithium:.*|lithium:x:`id -u`:`id -g`:lithium:/home/lithium:/bin/sh|" \
		/etc/passwd >/tmp/pulse-passwd
	else
	    cat /etc/group >/tmp/pulse-group
	    sed \
		"s|^lithium:.*|lithium:x:`id -u`:0:lithium:/home/lithium:/bin/sh|" \
		/etc/passwd >/tmp/pulse-passwd
	fi
    fi
    export NSS_WRAPPER_PASSWD=/tmp/pulse-passwd
    export NSS_WRAPPER_GROUP=/tmp/pulse-group
    export LD_PRELOAD=/usr/lib/libnss_wrapper.so
fi

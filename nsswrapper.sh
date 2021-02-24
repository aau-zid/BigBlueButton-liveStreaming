#!/bin/sh

if test "`id -u`" -ne 0; then
    if test -s /tmp/pulse-passwd; then
	echo Skipping nsswrapper setup - already initialized
    else
	echo Setting up nsswrapper mapping `id -u` to lithium
	sed "s|^audio:\(.*\)|audio:\1,lithium|" \
	    /etc/group >/tmp/pulse-group
	if test `id -g` -ne 0; then
	    echo "lithium:x:`id -g`:" >>/tmp/pulse-group
	fi
	(
	    cat /etc/passwd
	    echo "lithium:x:`id -u`:`id -g`:lithium:/home/lithium:/bin/sh"
	) >/tmp/pulse-passwd
    fi
    export NSS_WRAPPER_PASSWD=/tmp/pulse-passwd
    export NSS_WRAPPER_GROUP=/tmp/pulse-group
    export LD_PRELOAD=/usr/lib/libnss_wrapper.so
fi
export HOME=/home/lithium

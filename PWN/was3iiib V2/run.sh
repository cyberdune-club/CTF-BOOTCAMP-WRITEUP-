#!/bin/sh
set -eu
adduser --disabled-password --gecos "" ctf >/dev/null 2>&1 || true
chown -R root:root /challenge
chmod 755 /challenge/hft
chmod 444 /flag.txt
exec su -s /bin/sh -c "exec /challenge/entrypoint.sh" ctf

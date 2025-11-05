#!/bin/sh
set -eu
exec socat -dd -T 180 TCP-LISTEN:31344,reuseaddr,fork EXEC:"/challenge/hft",stderr
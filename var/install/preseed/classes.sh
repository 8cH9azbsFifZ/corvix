#!/bin/sh
set -e

. /usr/share/debconf/confmodule

db_get auto-install/classes && classes=$RET
classes=$(echo $RET |  sed -e 's/;/\n/g')
include=""
for c in $classes; do
   include="$include ../classes/$c/preseed.cfg "
done

db_set preseed/include "$include"

#!/bin/sh
set -e

. /usr/share/debconf/confmodule

db_get auto-install/classes && classes=$RET
[[ $classes == 10 ]] && exit 0
classes=$(echo $classes |  sed -e 's/;/\n/g')
include=""
for c in $classes; do
   include="$include ../classes/$c/preseed.cfg "
done

db_set preseed/include "$include"

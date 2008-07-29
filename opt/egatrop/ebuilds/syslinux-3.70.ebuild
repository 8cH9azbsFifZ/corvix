#!/bin/zsh
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

EBUILD=$0
. /opt/egatrop/lib/egatrop
ESRC_URI="http://www.kernel.org/pub/linux/utils/boot/$ENAME/$ENAME-$EVERS.tar.gz"
EMD5="09a4f2ca0c579497dc5c43415e9f05e6  $ENAME-$EVERS.tar.gz"
EWORK_DIR=
MIRROR=

_emerge
#_eautomake
#_einstall

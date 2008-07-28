#!/bin/zsh
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

EBUILD=$0
. /opt/egatrop/lib/egatrop
ESRC_URI="http://downloads.sourceforge.net/$ENAME/$ENAME-$EVERS.tar.gz"
EMD5="6b6d22662df5101b308c465a722c43ce  $ENAME-$EVERS.tar.gz"
EWORK_DIR=
MIRROR=

_ ./configure --prefix=$EBIN_DIR --with-readline=gnu
_ make -j 2
#_esu make install
_einstall

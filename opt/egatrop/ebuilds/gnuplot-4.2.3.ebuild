#!/bin/zsh
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

EBUILD=$0
. /opt/egatrop/lib/egatrop
ESRC_URI="http://downloads.sourceforge.net/$ENAME/$ENAME-$EVERS.tar.gz"
EDOC_URI="http://gerolf.ziegenhain.com/doc/gnuplot.pdf"
EMD5="6b6d22662df5101b308c465a722c43ce  $ENAME-$EVERS.tar.gz"
EWORK_DIR=
MIRROR=

_emerge
_eautomake --with-readline=gnu
_einstall

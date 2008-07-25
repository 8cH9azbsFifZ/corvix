#!/bin/zsh
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

EBUILD=$0
. ../lib/egatrop
ESRC_URI="http://downloads.sourceforge.net/$ENAME/$ENAME-$EVERS.tar.gz http://downloads.sourceforge.net/$ENAME/$ENAME-$EVERS.tar.bz2"

_efetch

_ tar xzf $ENAME-$EVERS.tar.gz
cd $ENAME-$EVERS
_ ./configure --prefix=$EBIN_DIR --with-readline=gnu
_ make -j 2
_esu make install

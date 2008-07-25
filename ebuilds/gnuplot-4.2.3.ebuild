#!/bin/zsh
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

EBUILD=$0
. /opt/egatrop/lib/egatrop
ESRC_URI="http://downloads.sourceforge.net/$ENAME/$ENAME-$EVERS.tar.gz"
_efetch
_ tar xzf $ENAME-$EVERS.tar.gz
cd $ENAME-$EVERS
_ ./configure --prefix=$EBIN_DIR --with-readline=gnu
_ make -j 2
_esu make install

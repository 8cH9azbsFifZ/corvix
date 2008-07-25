#!/bin/zsh
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

EBUILD=$0
ESRC_URI="http://downloads.sourceforge.net/$ENAME/$ENAME-$EVERS.tar.gz http://downloads.sourceforge.net/$ENAME/$ENAME-$EVERS.tar.bz2"
. ../lib/egatrop $EBUILD $ESRC_URI

#_efetch $SRC_URI
_ tar xzf $ENAME-$EVERS.tar.gz
cd $ENAME-$EVERS
_ ./configure --prefix=$EBIN_DIR --with-readline=gnu
_ make -j 2
_ make install

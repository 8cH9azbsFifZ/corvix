#!/bin/zsh
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

SRC_URI="http://downloads.sourceforge.net/$ENAME/$ENAME-$EVERS.tar.gz"

. /opt/egatrop/lib/egatrop

_efetch $ENAME-$EVERS.tar.gz
_ tar xzf $ENAME-$EVERS.tar.gz
cd $ENAME-$EVERS
_ ./configure --prefix=$EBIN_DIR --with-readline=gnu
_ make -j 2
_ make install

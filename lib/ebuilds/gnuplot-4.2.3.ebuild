#!/bin/zsh
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

. egatrop $0

SRC_URI="http://downloads.sourceforge.net/$ENAME/$ENAME-$EVERS.tar.gz"

_efetch $SRC_URI
_ tar xzf $ENAME-$EVERS.tar.gz
cd $ENAME-$EVERS
_ ./configure --with-readline=gnu --PREFIX=$EBIN_DIR
_ make -j 2 
_ make install

#!/bin/zsh
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

EBUILD=$0
. /opt/egatrop/lib/egatrop
ESRC_URI="http://downloads.sourceforge.net/$ENAME/$ENAME-$EVERS.tar.gz "
_efetch
_ tar xzf $EFULL.tar.gz
cd $EFULL
_ python setup.py config --compiler=unix build
_esu python setup.py config --compiler=unix install --prefix=$EBIN_DIR


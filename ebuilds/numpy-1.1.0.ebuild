#!/bin/zsh
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

EBUILD=$0
. /opt/egatrop/lib/egatrop
ESRC_URI="http://downloads.sourceforge.net/$ENAME/$ENAME-$EVERS.tar.gz"
EMD5="bf176b9857c4c588a63e414df84a1826  numpy-1.1.0.tar.gz"
_efetch
_emd5check
_ tar xzf $EFULL.tar.gz
cd $EFULL
_ python setup.py config --compiler=unix --fcompiler=gnu95 build
_esu python setup.py config --compiler=unix --fcompiler=gnu95 install --prefix=$EBIN_DIR

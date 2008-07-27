#!/bin/zsh
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

EBUILD=$0
. /opt/egatrop/lib/egatrop
ESRC_URI="http://downloads.sourceforge.net/$ENAME/$ENAME-$EVERS.tar.gz"
EMD5="417adf3bfe03f4c23c9fb265018e545c  scipy-0.6.0.tar.gz"
_efetch
_emd5check
_ tar xzf $EFULL.tar.gz
cd $EFULL

cat scipy/sandbox/setup.py | awk '/add_subpackage/&&/delaunay/{gsub("#","");print}{print}' > tmp
mv tmp scipy/sandbox/setup.py
_ python setup.py config --compiler=unix --fcompiler=gnu95 build 
_epython setup.py config --compiler=unix --fcompiler=gnu95 install --prefix=$EBIN_DIR

PAUSE "Adjust your PYTHONPATH=/opt/egatrop/lib/python2.5/site-packages"



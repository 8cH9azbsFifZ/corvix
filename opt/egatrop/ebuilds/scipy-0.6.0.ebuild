#!/bin/zsh
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

EBUILD=$0
. /opt/egatrop/lib/egatrop
ESRC_URI="http://downloads.sourceforge.net/$ENAME/$ENAME-$EVERS.tar.gz"
EMD5="417adf3bfe03f4c23c9fb265018e545c  $ENAME-$EVERS.tar.gz"
EDEP="numpy"

cat scipy/sandbox/setup.py | awk '/add_subpackage/&&/delaunay/{gsub("#","");print}{print}' > tmp
mv tmp scipy/sandbox/setup.py
export PYTHON_LIB=$EBIN_DIR/lib/python2.5/site-packages 
export PYTHONPATH=$EBIN_DIR/lib/python2.5/site-packages
export LAPACK=$EBIN_DIR/lib/libfblas.a
export BLAS=$EBIN_DIR/lib/libfblas.a
export INCPATH=$EBIN_DIR/include
[[ -e $BLAS ]] || DIE "Missing BLAS: $BLAS"

_emerge
_epython setup.py config --compiler=unix --fcompiler=gnu95 build 
_einstall

#PAUSE "Adjust your PYTHONPATH=/opt/egatrop/lib/python2.5/site-packages"


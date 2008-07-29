#!/bin/zsh
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

EBUILD=$0
. /opt/egatrop/lib/egatrop
ESRC_URI="http://downloads.sourceforge.net/$ENAME/$ENAME-$EVERS.tar.gz "
EMD5="1f673f82eb4f7422c1e45545f8e083d4  matplotlib-0.98.1.tar.gz"
EDEP="numpy"

PYTHON_LIB=$EBIN_DIR/lib/python2.5/site-packages 
PYTHONPATH=$EBIN_DIR/lib/python2.5/site-packages

_emerge
_epython setup.py config --compiler=unix build
_einstall

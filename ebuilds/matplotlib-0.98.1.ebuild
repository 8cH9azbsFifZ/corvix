#!/bin/zsh
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

EBUILD=$0
. /opt/egatrop/lib/egatrop
ESRC_URI="http://downloads.sourceforge.net/$ENAME/$ENAME-$EVERS.tar.gz "
EMD5="1f673f82eb4f7422c1e45545f8e083d4  matplotlib-0.98.1.tar.gz"
_efetch
_emd5check
_ tar xzf $EFULL.tar.gz
cd $EFULL
export PYTHON_LIB=$EBIN_DIR/lib/python2.5/site-packages 
export PYTHONPATH=$EBIN_DIR/lib/python2.5/site-packages
_ python setup.py config --compiler=unix build
_esu python setup.py config --compiler=unix install --prefix=$EBIN_DIR


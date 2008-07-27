#!/bin/egatrop -e
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

DESCRIPTION="python numpy"
HOMEPAGE=""
SRC_URI="http://downloads.sourceforge.net/$ENAME/$ENAME-$EVERS.tar.gz"

#DEPEND="g77 build-essential gfortran python-dev swig"
#SDEPEND="python-numpy"
#EDEPEND="umfpack"

LICENSE="abc"

#PREFIX=/usr/

src_compile() {
   cd $EFULL
   epython setup.py config --compiler=unix --fcompiler=gnu95 build 
}

src_install() {
   cd $EFULL
   epython setup.py config --compiler=unix --fcompiler=gnu95 install
}


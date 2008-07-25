#!/bin/egatrop -e
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

DESCRIPTION="python scipy"
HOMEPAGE=""
SRC_URI="http://prdownloads.sourceforge.net/$ENAME/$ENAME-$EVERS.tar.gz" 

DEPEND="build-essential gfortran python-dev swig"
SDEPEND="python-scipy python-matplotlib python-numpy"
EDEPEND="umfpack numpy"

LICENSE="abc"

src_configure() {
   cat scipy/sandbox/setup.py | awk '/add_subpackage/&&/delaunay/{gsub("#","");print}{print}' > tmp
   mv tmp scipy/sandbox/setup.py
}

src_compile() {
   cd $EFULL
   epython setup.py config --compiler=unix --fcompiler=gnu95 build 
}

src_install() {
   cd $EFULL
   epython setup.py config --compiler=unix --fcompiler=gnu95 install 
}


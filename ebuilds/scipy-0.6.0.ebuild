#!/bin/zsh
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

EBUILD=$0
. /opt/egatrop/lib/egatrop
ESRC_URI="http://downloads.sourceforge.net/$ENAME/$ENAME-$EVERS.tar.gz"
_efetch
_ tar xzf $EFULL.tar.gz
cd $EFULL

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


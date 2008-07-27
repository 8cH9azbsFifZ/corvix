#!/bin/egatrop -e
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

DESCRIPTION="matplotlib"
HOMEPAGE=""
SRC_URI="http://downloads.sourceforge.net/$ENAME/$ENAME-$EVERS.tar.gz "

DEPEND=""
SDEPEND="python-matplotlib-data python-matplotlib"
EDEPEND="scipy"

LICENSE="abc"

#PREFIX=/usr/

src_compile() {
   cd $EFULL
   epython setup.py config build 
}

src_install() {
   cd $EFULL
   epython setup.py config install
}


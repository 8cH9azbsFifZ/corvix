#!/bin/egatrop -e
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

DESCRIPTION="checkinstall"
HOMEPAGE="http://www.asic-linux.com.mx/~izto/checkinstall"
SRC_URI="$HOMEPAGE/files/source/$ENAME-$EVERS.tgz"

LICENSE="GPL-2"

src_compile() {
   cd $EDIRS
   emake -j 4
}

src_install() {
   cd $EDIRS
   einstall
}  

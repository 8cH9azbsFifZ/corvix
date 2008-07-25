#!/bin/egatrop -e
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

DESCRIPTION="Command-line driven interactive plotting program"
HOMEPAGE="http://www.gnuplot.info/"
SRC_URI="http://downloads.sourceforge.net/$ENAME/$ENAME-$EVERS.tar.gz"

LICENSE="gnuplot"

DEPEND="libreadline5 libreadline5-dev"
SDEPEND="gnuplot"

PREFIX=/usr/local

USE="readline"

src_configure() {
   euse readline && READLINE="--with-readline=gnu"
   cd $EFULL
   econfigure $READLINE
}

src_compile() {
   cd $EFULL
   emake -j  4
}

src_install() {
   cd $EFULL
   einstall
}

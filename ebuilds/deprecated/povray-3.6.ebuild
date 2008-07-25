#!/bin/egatrop -e
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

DESCRIPTION="povray"
HOMEPAGE="http://www.povray.org"
SRC_URI="http://www.povray.org/redirect/www.povray.org/ftp/pub/povray/Official/Unix/povray-$EVERS.tar.bz2"

LICENSE="abc"

PREFIX=/usr/local

src_configure() {
   cd $EDIRS
   econfigure COMPILED_BY="egatrop" --disable-io-restrictions
}

src_compile() {
   cd $EDIRS
   emake -j 4
}

src_install() {
   cd $EDIRS
   einstall
}  


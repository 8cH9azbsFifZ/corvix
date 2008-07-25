#!/bin/zsh
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

EBUILD=$0
. /opt/egatrop/lib/egatrop
ESRC_URI="http://www.povray.org/redirect/www.povray.org/ftp/pub/povray/Official/Unix/povray-$EVERS.tar.bz2"
_efetch
_ tar xjf povray-$EVERS.tar.bz2
cd povray-$EVERS.1
_ ./configure COMPILED_BY="egatrop" --disable-io-restrictions -without-x -without-svga --prefix=$EBIN_DIR
_ make -j 4
_esu make install

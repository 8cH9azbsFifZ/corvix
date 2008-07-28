#!/bin/zsh
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

EBUILD=$0
. /opt/egatrop/lib/egatrop
ESRC_URI="http://www.povray.org/redirect/www.povray.org/ftp/pub/povray/Official/Unix/povray-$EVERS.tar.bz2"
EMD5="b5789bb7eeaed0809c5c82d0efda571d  povray-3.6.tar.bz2"
EWORK_DIR=povray-$EVERS.1
_emerge

_eautomake COMPILED_BY="egatrop" --disable-io-restrictions -without-x -without-svga 
_einstall

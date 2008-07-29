#!/bin/zsh
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

EBUILD=$0
. /opt/egatrop/lib/egatrop
ESRC_URI="http://www.mcs.anl.gov/research/projects/$ENAME/downloads/tarballs/$ENAME-$EVERS.tar.gz"
EDOC_URI="http://www.mcs.anl.gov/research/projects/$ENAME/documentation/files/$ENAME-doc-user.pdf"
EMD5="c3beb9430d45347078a80cf1c6780509  $ENAME-$EVERS.tar.gz"
EWORK_DIR=
MIRROR=

_emerge
NCPU=1
_eautomake --disable-romio --enable-sharedlibs=gcc --with-thread-package=posix --with-device=p4
_einstall

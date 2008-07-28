#!/bin/zsh
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

EBUILD=$0
. /opt/egatrop/lib/egatrop
ESRC_URI="http://www.cise.ufl.edu/research/sparse/umfpack/current/UMFPACK.tar.gz http://www.cise.ufl.edu/research/sparse/UFconfig/current/UFconfig.tar.gz http://www.cise.ufl.edu/research/sparse/amd/current/AMD.tar.gz"
EMD5="
f81fcae945de82864035b03ee20a8d2b  AMD.tar.gz
331ec33d1df77fb7d9ee359a7f2d6ee3  UFconfig.tar.gz
8ad2d68c7c49dfcdd8321e806e6c611c  UMFPACK.tar.gz
"
EWORK_DIR=$ESRC_DIR

prepare() {
   [[ -d umfpack ]] || mkdir umfpack
   cd umfpack
   _einstall --mode=oag+rx UFconfig/UFconfig.h $EBIN_DIR/include/UFconfig.h
}

make_amd() {
   LOG "   Compile AMD"
   cd AMD
   _ make
   cd ..
   _einstall --mode=oag+rx AMD/Lib/libamd.a $EBIN_DIR/lib/libamd.a
   _einstall --mode=oag+rx AMD/Include/amd.h $EBIN_DIR/include/amd.h
}

make_umfpack() {
   LOG "Compile umfpack"
   cd UMFPACK
   _ make
   cd ..
   _einstall --mode=oag+rx UMFPACK/Lib/libumfpack.a $EBIN_DIR/lib/libumfpack.a 
   for f in UMFPACK/Include/*.h; do
      _einstall --mode=oag+rx $f $EBIN_DIR/include/$(basename $f)
   done
}

_emerge
prepare
make_amd
make_umfpack

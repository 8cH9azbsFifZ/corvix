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
_efetch
_emd5check

prepare() {
   [[ -d umfpack ]] || mkdir umfpack
   cd umfpack

   _ tar xzf ../UFconfig.tar.gz
   _esu install --mode=oag+rx UFconfig/UFconfig.h $EBIN_DIR/include
}

make_amd() {
   LOG "   Compile AMD"
   _ tar xzf ../AMD.tar.gz
   cd AMD
   _ make
   cd ..
   _esu install --mode=oag+rx AMD/Lib/libamd.a $EBIN_DIR/lib
   _esu install --mode=oag+rx AMD/Include/amd.h $EBIN_DIR/include
}

make_umfpack() {
   LOG "Compile umfpack"
   cd UMFPACK
   _ tar xzf ../UMFPACK.tar.gz
   _ make
   cd ..
   _esu install --mode=oag+rx UMFPACK/Lib/libumfpack.a $EBIN_DIR/lib
   _esu install --mode=oag+rx UMFPACK/Include/*.h $EBIN_DIR/include
}


prepare
make_amd
make_umfpack

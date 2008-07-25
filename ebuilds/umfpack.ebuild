#!/bin/zsh
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

EBUILD=$0
. /opt/egatrop/lib/egatrop
SRC_URI="http://www.cise.ufl.edu/research/sparse/umfpack/current/UMFPACK.tar.gz http://www.cise.ufl.edu/research/sparse/UFconfig/current/UFconfig.tar.gz http://www.cise.ufl.edu/research/sparse/amd/current/AMD.tar.gz"
_efetch


src_configure() {
   esu install --mode=oag+rx UFconfig/UFconfig.h $PREFIX/include
}

compile_amd() {
   LOG "   Compile AMD"
   _ tar xzf AMD.tar.gz
   cd AMD
   _ make
   cd ..
}

compile_umfpack() {
   elog "Compile umfpack"
   cd UMFPACK
   emake
   cd ..
}

install_amd() {
   esu install --mode=oag+rx AMD/Lib/libamd.a $PREFIX/lib
   esu install --mode=oag+rx AMD/Include/amd.h $PREFIX/include
}

install_umfpack() {
   esu install --mode=oag+rx UMFPACK/Lib/libumfpack.a $PREFIX/lib
   esu install --mode=oag+rx UMFPACK/Include/*.h $PREFIX/include
   EDIRS=$ETMP/UMFPACK
}

src_install() {
   install_amd
   install_umfpack
}

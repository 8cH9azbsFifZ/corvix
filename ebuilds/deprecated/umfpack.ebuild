#!/bin/egatrop -e
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

DESCRIPTION="Unsymmetric multifrontal sparse LU factorization library (umfpack / amd/ ufconfig)"
HOMEPAGE="http://www.cise.ufl.edu/research/sparse/umfpack"
SRC_URI="http://www.cise.ufl.edu/research/sparse/umfpack/current/UMFPACK.tar.gz http://www.cise.ufl.edu/research/sparse/UFconfig/current/UFconfig.tar.gz http://www.cise.ufl.edu/research/sparse/amd/current/AMD.tar.gz"

#DEPEND="blas"
#SDEPEND="blas"

LICENSE="GPL-2 / LGPL-2.1 / LGPL-2"

PREFIX=/usr

src_configure() {
   esu install --mode=oag+rx UFconfig/UFconfig.h $PREFIX/include
}

compile_amd() {
   elog "Compile AMD"
   cd AMD
   emake
   cd ..
}

compile_umfpack() {
   elog "Compile umfpack"
   cd UMFPACK
   emake
   cd ..
}

src_compile() {
   compile_amd
   compile_umfpack
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

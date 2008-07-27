#!/bin/egatrop -e
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

DESCRIPTION="lapack"
HOMEPAGE=""
SRC_URI="http://www.netlib.org/blas/blas.tgz http://www.netlib.org/lapack/lapack.tgz"

DEPEND="build-essential gfortran python-dev swig"
SDEPEND="python-scipy python-matplotlib python-numpy"
EDEPEND=""

LICENSE="abc"

PREFIX=/usr/

make_blas() {
   BLAS=/lib/libfblas.a
   [[ -e $BLAS ]] && return 0
   #rr g77 -fno-second-underscore -O2 -c *.f
   emake -j 4 
   rr ar r libfblas.a *.o
   rr ranlib libfblas.a
   #rr rm -rf *.o
   esu install --mode=aog+rx libfblas.a /lib
}

make_lapack() {
   cp INSTALL/make.inc.LINUX make.inc 
      # Edit make.inc as follows:
      PLAT = _Linux
      OPTS = -O2
   make lapacklib
   make clean
   cp lapack_LINUX.a libflapack.a                 # on LINUX
   LAPACK=~/src/LAPACK/libflapack.a
   #NOTE: scipy may not find the libf* names.  You may have to make a symbolic link from these files to libblas.a and liblapack.a  Numpy does not seem to have this problem.
}

src_compile() {
}

src_install() {
}


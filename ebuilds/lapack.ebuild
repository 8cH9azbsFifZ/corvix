#!/bin/zsh
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

EBUILD=$0
. /opt/egatrop/lib/egatrop
ESRC_URI="http://www.netlib.org/blas/blas.tgz http://www.netlib.org/lapack/lapack.tgz"
_efetch

make_blas() {
   LOG "   Make blas"
   BLAS=/lib/libfblas.a
   [[ -e $BLAS ]] && return 0
   _ tar xzf blas.tgz
   cd BLAS
   _ gfortran -c *.f
   _ ar r libfblas.a *.o
   _ ranlib libfblas.a
   _esu install --mode=aog+rx libfblas.a /lib
}

make_lapack() {
   LOG "    Make lapack"
   cp INSTALL/make.inc.LINUX make.inc 
      # Edit make.inc as follows:
      PLAT = _Linux
      OPTS = -O2
   _ make lapacklib
   _ make clean
   cp lapack_LINUX.a libflapack.a                 # on LINUX
   LAPACK=~/src/LAPACK/libflapack.a
   #NOTE: scipy may not find the libf* names.  You may have to make a symbolic link from these files to libblas.a and liblapack.a  Numpy does not seem to have this problem.
}



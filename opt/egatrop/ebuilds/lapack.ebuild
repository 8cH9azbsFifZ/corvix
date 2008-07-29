#!/bin/zsh
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

EBUILD=$0
. /opt/egatrop/lib/egatrop
ESRC_URI="http://www.netlib.org/blas/blas.tgz http://www.netlib.org/lapack/lapack.tgz"
EMD5="
7e6af7022440d8688d16be86d55fb358  blas.tgz
00b21551a899bcfbaa7b8443e1faeef9  lapack.tgz
"
MIRROR=http://mirror.corvix.eu
EWORK_DIR=$ESRC_DIR


BLAS=$EBIN_DIR/lib/libfblas.a

make_blas() {
   LOG "   Make blas"
   [[ -e $BLAS ]] && return 0
   _ tar xzf blas.tgz
   cd BLAS
   _ gfortran -c *.f
   _ ar r libfblas.a *.o
   _ ranlib libfblas.a
   _einstall --mode=aog+rx libfblas.a $EBIN_DIR/lib/libfblas.a
   cd ..
}

patch_lapack() {
   LOG "   patching lapack for gfortran (EXTERNAL ETIME bug)"
   cat INSTALL/dsecnd_EXT_ETIME.f | awk  'NR!=23' >/tmp/123
   mv /tmp/123 INSTALL/dsecnd_EXT_ETIME.f
   cat INSTALL/second_EXT_ETIME.f | awk  'NR!=23' >/tmp/123
   mv /tmp/123 INSTALL/second_EXT_ETIME.f
}

make_lapack() {
   LOG "    Make lapack"
   _ tar xzf lapack.tgz
   cd lapack-3.1.1
   cp INSTALL/make.inc.LINUX make.inc 
   cat make.inc | sed 's/g77/gfortran/g' > /tmp/123
   mv /tmp/123 make.inc
   _ make lapacklib
   LOG "This one had to fail :/"
   patch_lapack
   _ make lapacklib
   cp lapack_LINUX.a libflapack.a                 # on LINUX
   _einstall --mode=aog+rx libflapack.a $EBIN_DIR/lib/libflapack.a
   #NOTE: scipy may not find the libf* names.  You may have to make a symbolic link from these files to libblas.a and liblapack.a  Numpy does not seem to have this problem.
}

_emerge

make_blas
make_lapack

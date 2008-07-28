#!/bin/zsh
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

EBUILD=$0
. /opt/egatrop/lib/egatrop
ver_maui=3.2.6p19
ver_torque=2.1.6
ESRC_URI="http://www.clusterresources.com/downloads/torque/torque-$ver_torque.tar.gz http://www.clusterresources.com/downloads/maui/maui-$ver_maui.tar.gz"
EMD5="1f673f82eb4f7422c1e45545f8e083d4  matplotlib-0.98.1.tar.gz"
EWORK_DIR=$ESRC_DIR
_emerge

_compile_torque() {
   LOG "   Compiling torque"
   cd /usr/src/cluster/torque-$ver_torque
   _ ./configure --enable-server --enable-monitor --enable-clients --enable-syslog
   _ make -j 2
   _ make install
}   
_compile_maui() {   
   LOG "   Compiling Maui"
   cd /usr/src/cluster/maui-$ver_maui
   export MAUIADMIN=root
   _ ./configure --with-spooldir=/var/spool/torque --with-pbs=/usr/local
   _ make -j 2
   _ make install
}

_postinstall() {
   LOG "   Postinstall stuff"
   _ chmod aog+rwx /var/spool/torque/spool
}

#_prepare
#_compile_torque
#_compile_maui
#_postinstall

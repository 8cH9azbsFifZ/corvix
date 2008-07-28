#!/bin/zsh
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

EBUILD=$0
. /opt/egatrop/lib/egatrop
ver_maui=3.2.6p19
ver_torque=2.1.6
ESRC_URI="http://www.clusterresources.com/downloads/torque/torque-$ver_torque.tar.gz http://www.clusterresources.com/downloads/maui/maui-$ver_maui.tar.gz"
EMD5="
abfeb1a3a5aa53f725f975c2b5d98e1e  torque-$ver_torque.tar.gz
ec66489f57f8ee9e6943c0910b4631d4  maui-$ver_maui.tar.gz
"
EWORK_DIR=$ESRC_DIR

_compile_torque() {
   LOG "Compiling torque"
   cd torque-$ver_torque
   _eautomake --enable-server --enable-monitor --enable-clients --enable-syslog
   _einstall
   cd ..
}   
_compile_maui() {   
   LOG "Compiling Maui"
   cd maui-$ver_maui
   export MAUIADMIN=root
   _eautomake --with-spooldir=/var/spool/torque --with-pbs=$EBIN_DIR
   _einstall
}

_postinstall() {
   LOG "Postinstall stuff"
   _ chmod aog+rwx $EBIN_DIR/var/spool/torque/spool
}

_emerge
_compile_torque
_compile_maui

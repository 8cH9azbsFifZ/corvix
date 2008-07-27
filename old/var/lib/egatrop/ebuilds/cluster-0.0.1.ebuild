#!/bin/egatrop -e
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

USE="server"

SHELLS="ash zsh bash csh ksh"
BUILD="build-essential g++ g++-3.4 g++-4.1 g77 gcc gcc-3.4 gcc-4.1 gfortran"
VCS="cvs subversion git-core"
PLOT="imagemagick mencoder mplayer w32codecs"
CALC="octave "
SNAKE="ipython"
EDITORS="joe vim-full emacs"
ADMIN="less most psutils psmisc rsync gawk ganglia-monitor librrd2 nfs-common portmap ntpdate"
SRV="arping mtools xinetd syslinux dhcp tftp-hpa apache2 psmisc"
BROWSE="lynx links links2 wget"
NET="tcpdump ettercap"
MPI="mpich-bin libmpich1.0c2 libmpich1.0-dev"
SIM="gromacs gromacs-mpich"
LOGIN="ssh rsh-redone-client rsh-redone-client"
PAK="bzip2"



PKGS="$SHELLS $BUILD $VCS $PLOT $CALC $EDITORS $ADMIN $BROWSE $NET $SNAKE $MPI $SIM $LOGIN $PAK"
euse server && PKGS=$PKGS" $SRV"

DEPEND=$PKGS
SDEPEND=$DEPEND

src_preinst() {
   esu debian-sources
   esu apt-get update
   esu apt-get -y --force-yes install debian-multimedia-keyring
}

debian-sources() {   
cat << eof >> /etc/apt/sources.list   

deb http://head/ftp.uni-kl.de/debian/ etch main contrib non-free
deb-src http://head/ftp.uni-kl.de/debian/ etch main contrib non-free

deb http://head/security.debian.org/ etch/updates main contrib non-free
deb-src http://head/security.debian.org/ etch/updates main contrib non-free

#deb http://head/ftp.uni-kl.de/debian-local etch-unikl main unikl

deb http://head/debian.netcologne.de/debian-multimedia.org/ etch main
deb-src http://head/debian.netcologne.de/debian-multimedia.org/ etch main
eof
}

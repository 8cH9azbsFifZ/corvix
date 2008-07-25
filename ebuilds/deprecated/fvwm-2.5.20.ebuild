#!/bin/egatrop -e
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

DESCRIPTION="fvwm"
HOMEPAGE="http://www.fvwm.org"
SRC_URI="ftp://ftp.fvwm.org/pub/fvwm/version-2/fvwm-$EVERS.tar.bz2 http://www.abdn.ac.uk/~u15dm4/fvwm/VariousPatches6.patch"

DEPEND="aterm gmrun trayer habak conky gsetroot vim-outliner rxvt-unicode rxvt xterm unclutter ipython picasa thunar k3b pidgin kphone"
SDEPEND="fvwm"

LICENSE="abc"

PREFIX=/usr/local

src_configure() {
   #epatch ../fvwm-translucency.diff 
   rr autoconf
   rr aclocal
   rr automake
   econfigure --disable-bidi
}

src_compile() {
   emake -j 4
}

src_install() {
   einstall
}  

post_inst() {
   elog "Installing Theme..."
}

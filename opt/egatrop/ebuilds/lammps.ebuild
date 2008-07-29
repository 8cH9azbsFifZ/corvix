#!/bin/zsh
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

EBUILD=$0
. /opt/egatrop/lib/egatrop
ESRC_URI="http://lammps.sandia.gov/tars/lammps-upgrade.tar.gz"
_efetch
_ tar xzf lammps-upgrade.tar.gz

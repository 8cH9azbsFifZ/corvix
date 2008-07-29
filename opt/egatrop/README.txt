Files:
======
- todo.otl:
   vim outliner file with project track
- /opt/egatrop:
   egatrops directory structure


Mirror support:
===============
Simply set a mirror variable:
MIRROR=mirror.corvix.eu

Functions in ebuilds:
=====================
_efetch: 
   if needed, download the ESRC_URI files
_emd5check:
   check the md5sums of the ESRC_URI files with the EMD5 checksums
_ename:
   set variables from EBUILD_NAME
_esu:
   sudo wrapper
_eautomake:
   ./configure... ; make 
_epython:
   python setup.py ...
_eunpack:
   unpacking of archive ...
_einstall:
   wrapper for
   (a) python install 
   (b) automake install
   (c) manual install, last argument has to be installed file(!)
   wrapper for "make install" will write installed files to ILOG

Variables in ebuilds:
=====================
ILOG:
   logfile of installed files
EDOC_URI:
   additional documentation files; will be installed automatically
EDEP:
   dependencies (resolved by egatrop)
EDEP_DEB:
   dependencies (resolved by debian)

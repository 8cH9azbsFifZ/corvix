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
_epython:
   python wrapper - includes tracking of installed files for simple uninstalls
_einstall:
   wrapper for "make install" will write installed files to ILOG

Variables in ebuilds:
=====================
ILOG:
   logfile of installed files
   

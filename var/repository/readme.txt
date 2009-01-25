How to use: in /etc/sources.list:
deb http://corvix.eu testing meta ware


Key signatures:
#gpg --export -a corvix.eu > corvix.eu.pub
gpg --keyserver pgpkeys.mit.edu --recv-key 974E7D68
gpg -a --export 974E7D68 | sudo apt-key add -


deb file:///home/gerolf/gnu/debian/repository testing/

key:
gpg --export -a corvix.eu > corvix.eu.pub
gpg --keyserver pgpkeys.mit.edu --recv-key 37A46DF5974E7D68
gpg -a --export 37A46DF5974E7D68 | sudo apt-key add -


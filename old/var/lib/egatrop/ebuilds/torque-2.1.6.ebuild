#!/bin/egatrop -e
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

DESCRIPTION="Cluster queue system"
HOMEPAGE="http://www.clusterresources.com"
SRC_URI="http://www.clusterresources.com/downloads/torque/$EFULL.tar.gz"

LICENSE="abc"

SE="server"

src_configure() {
   euse server && econfigure --enable-server
   euse server || econfigure --disable-server
}

src_compile() {
   cd $EFULL
   emake -j 4
}

src_install() {
   cd $EFULL
   einstall
   create_client
   euse server && create_server
}

src_postinst() {
   hints   
}

hints() {
cat << eof
$red Edit /etc/cluster/* $none
eof   
}

create_client() {
[[ ! -e /etc/cluster/queue ]] && esu mkdir -p /etc/cluster/queue

esu echo QUEUE_SERVER > /etc/cluster/queue/server_name
[[ -e /var/spool/torque/server_name ]] && esu rm /var/spool/torque/server_name
esu ln -s /etc/cluster/queue/server_name /var/spool/torque/server_name

esu touch /etc/cluster/queue/config
esu chmod oag+rwx /etc/cluster/queue/config
cat << eof > /etc/cluster/queue/config
\$pbsserver QUEUE_SERVER
\$logevent 255 
\$max_load 2
eof
esu chmod og-rwx /etc/cluster/queue/config
[[ -e /var/spool/torque/mom_priv/config ]] && esu rm /var/spool/torque/mom_priv/config
esu ln -s /etc/cluster/queue/config /var/spool/torque/mom_priv/config
}

create_server() {
[[ ! -e /etc/cluster/queue ]] && esu mkdir -p /etc/cluster/queue
esu echo NODES_HERE > /etc/cluster/queue/nodes
[[ -e /var/spool/torque/mom_priv/server_priv/nodes ]] && esu rm /var/spool/torque/mom_priv/server_priv/nodes
esu ln -s /etc/cluster/queue/nodes /var/spool/torque/mom_priv/server_priv/nodes
[[ -e /var/spool/torque/maui.cfg ]] && esu rm /var/spool/torque/maui.cfg
esu ln -s /etc/cluster/queue/maui.cfg /var/spool/torque/maui.cfg
}



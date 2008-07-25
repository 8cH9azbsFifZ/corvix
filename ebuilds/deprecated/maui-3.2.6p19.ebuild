#!/bin/egatrop -e
# (C)opyleft Gerolf Ziegenhain <gerolf@ziegenhain.com> 2008

DESCRIPTION="Cluster queue system"
HOMEPAGE="http://www.clusterresources.com"
SRC_URI="http://www.clusterresources.com/downloads/maui/$EFULL.tar.gz"

LICENSE="abc"

src_configure() {
   MAUIADMIN=root
   econfigure --with-spooldir=/var/spool/torque --with-pbs=/usr/local
}

src_compile() {
   cd $EFULL
   emake -j 4
}

src_install() {
   cd $EFULL
   einstall
   create_mauicfg
}

create_mauicfg() {
[[ ! -e /etc/cluster/queue ]] && esu mkdir -p /etc/cluster/queue
esu touch /etc/cluster/queue/maui.cfg
esu chmod ao+rwx /etc/cluster/queue/maui.cfg
cat << eof > /etc/cluster/queue/maui.cfg   
SERVERHOST            QUEUE_SERVER
ADMIN1                root
RMCFG[base] TYPE=PBS 
AMCFG[bank]  TYPE=NONE
RMPOLLINTERVAL        00:00:30
SERVERPORT            42559
SERVERMODE            NORMAL
LOGFILE               maui.log
LOGFILEMAXSIZE        10000000
LOGLEVEL              3
QUEUETIMEWEIGHT       1 

#FSPOLICY              PSDEDICATED
#FSDEPTH               7
#FSINTERVAL            86400
#FSDECAY               0.80

#FIXME :(
NODECFG[node1] PARTITION=cluster
NODECFG[node2] PARTITION=cluster
NODECFG[node3] PARTITION=cluster
NODECFG[node4] PARTITION=cluster
NODECFG[node5] PARTITION=cluster
NODECFG[node6] PARTITION=cluster
NODECFG[node7] PARTITION=cluster
NODECFG[node8] PARTITION=cluster
NODECFG[node9] PARTITION=cluster
NODECFG[node10] PARTITION=cluster
NODECFG[node11] PARTITION=cluster
NODECFG[node12] PARTITION=cluster
NODECFG[node13] PARTITION=cluster
NODECFG[node14] PARTITION=cluster
NODECFG[node15] PARTITION=cluster
NODECFG[node16] PARTITION=cluster
NODECFG[node17] PARTITION=cluster
NODECFG[node18] PARTITION=cluster
NODECFG[node19] PARTITION=cluster
NODECFG[node20] PARTITION=cluster
NODECFG[node21] PARTITION=cluster
NODECFG[node22] PARTITION=cluster
NODECFG[node23] PARTITION=cluster
NODECFG[node24] PARTITION=cluster
NODECFG[node25] PARTITION=cluster
NODECFG[node26] PARTITION=cluster
NODECFG[node27] PARTITION=cluster
NODECFG[node28] PARTITION=cluster
NODECFG[node29] PARTITION=cluster
NODECFG[node30] PARTITION=cluster
NODECFG[node31] PARTITION=cluster
NODECFG[node32] PARTITION=cluster
NODECFG[node33] PARTITION=cluster
NODECFG[node34] PARTITION=cluster
NODECFG[node35] PARTITION=cluster
NODECFG[node36] PARTITION=cluster
NODECFG[node37] PARTITION=cluster
NODECFG[node38] PARTITION=cluster
NODECFG[node39] PARTITION=cluster
NODECFG[node40] PARTITION=cluster

NODECFG[nigol1] PARTITION=login
NODECFG[nigol2] PARTITION=login

SYSCFG[base]     PLIST=

BACKFILLPOLICY        FIRSTFIT
RESERVATIONPOLICY     CURRENTHIGHEST

NODEALLOCATIONPOLICY  MINRESOURCE

# QOSCFG[hi]  PRIORITY=100 XFTARGET=100 FLAGS=PREEMPTOR:IGNMAXJOB
# QOSCFG[low] PRIORITY=-1000 FLAGS=PREEMPTEE

RESOURCELIMITPOLICY  MEM:ALWAYS:CANCEL
ENFORCERESOURCELIMITS ON
CREDWEIGHT      1     
USERWEIGHT      1
GROUPWEIGHT     1


# USERCFG[DEFAULT]      FSTARGET=25.0
# USERCFG[john]         PRIORITY=100  FSTARGET=10.0-
# GROUPCFG[staff]       PRIORITY=1000 QLIST=hi:low QDEF=hi
# CLASSCFG[batch]       FLAGS=PREEMPTEE
# CLASSCFG[interactive] FLAGS=PREEMPTOR

#GROUPCFG[DEFAULT] MAX
GROUPCFG[urbassek]   MAXJOB=5,10    MAXNODES=40,40 MAXPROC=160,160   PLIST=cluster PDEF=cluster
eof
esu chmod og-wx /etc/cluster/queue/maui.cfg
[[ -e /var/spool/torque/maui.cfg ]] && esu rm /var/spool/torque/maui.cfg
esu ln -s /etc/cluster/queue/maui.cfg /var/spool/torque/maui.cfg
}

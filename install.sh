#!/bin/bash
if [ "$(id -u)" != "0" ]; then
   echo "This script must be run as root" 1>&2
   exit 1
fi

echo "chmod"
chmod +x plugins/solr_*
chown root:root plugins/solr_*
mv plugins/solr_* /usr/share/munin/plugins/
ln -s /usr/share/munin/plugins/solr_docs /etc/munin/plugins/solr_docs
ln -s /usr/share/munin/plugins/solr_documentcache /etc/munin/plugins/solr_documentcache
ln -s /usr/share/munin/plugins/solr_filtercache /etc/munin/plugins/solr_filtercache
ln -s /usr/share/munin/plugins/solr_qps /etc/munin/plugins/solr_qps
ln -s /usr/share/munin/plugins/solr_querycache /etc/munin/plugins/solr_querycache
ln -s /usr/share/munin/plugins/solr_querytime /etc/munin/plugins/solr_querytime
ln -s /usr/share/munin/plugins/solr_updates /etc/munin/plugins/solr_updates
echo "restarting munin-node and running scripts"
/etc/init.d/munin-node restart
/etc/munin/plugins/solr_docs
/etc/munin/plugins/solr_documentcache
/etc/munin/plugins/solr_filtercache
/etc/munin/plugins/solr_qps
/etc/munin/plugins/solr_querycache
/etc/munin/plugins/solr_querytime
/etc/munin/plugins/solr_updates

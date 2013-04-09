# JVM Monitoring

This plugin will monitor the heap used by the VM specified in the pid file (which is configurable)

## Installation

* Copy jstat_heap into /usr/share/munin/plugins
* chmod u+x /usr/share/munin/plugins/jstat_heap
* sudo ln -s /usr/share/munin/plugins/jstat_heap /etc/munin/plugins/jstat_heap
* sudo /etc/munin/plugin-conf.d/munin-node

        [jstat_heap]
        user root

 * sudo /etc/init.d/munin-node stop
 * sudo /etc/init.d/munin-node start
 * Wait for next munin-update from munin server.

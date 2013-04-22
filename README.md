# DGU Monitoring extensions

## Nagios plugins

### cron monitoring

A plugin to check that cron jobs that we have scheduled execute when we would expect.


## Munin plugins for DGU

A collection of plugins for munin to show how the systems are behaving

### JVM plugin for Munin

The plugin is based on the jstat_heap plugin from [Munin monitoring](http://munin-monitoring.org/browser/munin-contrib/plugins/java/jstat__heap) and monitors heap usage within the JVM used for Solr.

### Solr Plugins for Munin

This code is a fork of [https://github.com/kura/solr-munin](https://github.com/kura/solr-munin) which itself is a fork of [https://github.com/distilledmedia/munin-plugins](https://github.com/distilledmedia/munin-plugins)

The install script has been changed, and the port on which Solr is contacted is set to the default.
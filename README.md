# py_check_elastic
nagios plugins to check elasticsearch state

please see requirements

usage:
Usage: check_elastic.py [options]

Options:

  --version             show program's version number and exit
  
  -h, --help            show this help message and exit
  
  
  -v, --verbose
  
  
  -H HOST, --host=HOST  The cluster or node to check
  
  
  -P PORT, --port=PORT  The ES port (default port is 9200
  
example: return

green cluster name: testcluster nodes : 2, master: name_master slave: [u'slave1', u'slave2'] unassigned_shards: 0

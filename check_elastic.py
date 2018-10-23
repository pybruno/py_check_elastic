# coding: utf-8
import requests
from nagioscheck import NagiosCheck
from nagioscheck import Status


class ElasticCheck(NagiosCheck):
    """
    momitor ES health and number of nodes and master ans slave
    """
    def __init__(self):
        NagiosCheck.__init__(self)
        self.add_option('H', 'host', 'host', 'The cluster or node to check')
        self.add_option('P', 'port', 'port', 'The ES port')
        self.slave = []

    def check(self, opts, args):
        if opts.host:
            host = opts.host
            port = int(opts.port or '9200')
        else:
            raise Status(Status.EXIT_CRITICAL, 'plz set host')

        try:
            cluster_status = requests.get('http://%s:%d/_cluster/health' % (host, port)).json()
            cluster_info = requests.get('http://%s:%d/_cluster/state' % (host, port)).json()

        except Exception as e:
            raise Status(Status.EXIT_CRITICAL, "can't connect to ES server")

        if cluster_status['number_of_data_nodes'] >= 2:
            nbr_node = int(cluster_status['number_of_data_nodes'])
            master_id = cluster_info['master_node']
            master = cluster_info['nodes'][master_id]['name']
            unassigned_shards = cluster_status['unassigned_shards']
            cluster_info['nodes'].pop(master_id)
            cluster_name = cluster_status['cluster_name']
            for key in cluster_info['nodes']:
                self.slave.append(cluster_info['nodes'][key]['name'])
        else:
            nbr_node = 1
            master_id = cluster_info['master_node']
            unassigned_shards = cluster_status['unassigned_shards']
            master = cluster_info['nodes'][master_id]['name']
            self.slave = None
            cluster_name = cluster_status['cluster_name']

        info_master = "cluster name: {} nodes : {}, master: {} slave: {} unassigned_shards: {}"\
            .format(cluster_name, nbr_node, master, self.slave, unassigned_shards)

        if cluster_status['status'].lower() == 'red':
            raise Status(Status.EXIT_CRITICAL, "RED {}".format(info_master))
        elif cluster_status['status'].lower() == 'yellow':
            raise Status(Status.EXIT_WARNING, "yellow {}".format(info_master))
        elif cluster_status['status'].lower() == 'green':
            raise Status(Status.EXIT_OK, "green {}".format(info_master))

        else:
            raise Status(Status.EXIT_UNKNOWN, ("no info",))


if __name__ == "__main__":
    ElasticCheck().run()

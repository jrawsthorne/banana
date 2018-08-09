import json

from fabric.api import env
from prepare import all_servers, Prepare


class GCPPrepare(Prepare):

    def __init__(self, details_file):
        self.details_file = details_file
        env.user = 'root'
        env.password = 'couchbase'
        self.ip_list_public_dns = []
        self.create_environment()

    def create_environment(self):
        with open(self.details_file, 'r') as f:
            data_store = json.load(f)

        for server in data_store:
            self.ip_list_public_dns.append(server["networkInterfaces"][0]["accessConfigs"][0]["natIP"])

        print(self.ip_list_public_dns)

    @all_servers
    def make_ssh_ready(self):
        pass

    def make_ips_file(self):
        servers = "\",\"".join(self.ip_list_public_dns)
        servers = "\"" + servers + "\""
        with open(self.IP_FILE, "w") as fp:
            fp.write(servers)

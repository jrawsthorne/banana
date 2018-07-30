import json

from fabric.api import env, run
from prepare import all_servers, Prepare


class AzurePrepare(Prepare):

    def __init__(self, details_file):
        self.details_file = details_file
        env.user = 'Administrator'
        env.password = 'password'
        self.ip_list_public_dns = []
        self.create_environment()

    def create_environment(self):
        with open(self.details_file, 'r') as f:
            data_store = json.load(f)

        for server in data_store:
            self.ip_list_public_dns.append(server["dnsSettings"]["fqdn"])

        print(self.ip_list_public_dns)

    @all_servers
    def make_ssh_ready(self):
        run("echo 'couchbase' | sudo passwd")
        run("sudo sed -i '/PermitRootLogin without-password/c\PermitRootLogin yes' /etc/ssh/sshd_config")
        run("sudo service ssh restart")

    def make_ips_file(self):
        servers = "\",\"".join(self.ip_list_public_dns)
        servers = "\"" + servers + "\""
        with open(self.IP_FILE, "w") as fp:
            fp.write(servers)

import json

from fabric.api import env, run
from prepare import all_servers, Prepare


class AWSPrepare(Prepare):
    STACK_NAME = "a-test"

    def __init__(self, details_file, key_file, stack_name):
        self.details_file = details_file
        self.stack_name = self.STACK_NAME
        if isinstance(stack_name, basestring):
            self.stack_name = stack_name
        env.user = 'ec2-user'
        env.key_filename = key_file
        self.ip_list_public_dns = []
        self.create_environment()

    def create_environment(self):
        with open(self.details_file, 'r') as f:
            data_store = json.load(f)

        reservations = data_store["Reservations"]

        ip_list_private = []
        for reservation in reservations:
            instances = reservation["Instances"]
            for instance in instances:
                if "Tags" in instance:
                    tags = instance["Tags"]
                else:
                    continue
                for tag in tags:
                    if tag["Key"] == "aws:cloudformation:stack-name" and tag["Value"] == self.stack_name:
                        if "PublicIpAddress" in instance:
                            self.ip_list_public_dns.append(instance["PublicDnsName"])
                            ip_list_private.append(instance["PrivateIpAddress"])

        print(self.ip_list_public_dns)
        print(ip_list_private)

    @all_servers
    def make_ssh_ready(self):
        run("echo 'couchbase' | sudo passwd --stdin root")
        run("sudo sed -i '/#PermitRootLogin yes/c\PermitRootLogin yes' /etc/ssh/sshd_config")
        run("sudo sed -i '/PermitRootLogin forced-commands-only/c\#PermitRootLogin "
            "forced-commands-only' /etc/ssh/sshd_config")
        run("sudo sed -i '/PasswordAuthentication no/c\PasswordAuthentication yes' "
            "/etc/ssh/sshd_config")
        run("sudo service sshd restart")

    def make_ips_file(self):
        servers = "\",\"".join(self.ip_list_public_dns)
        servers = "\"" + servers + "\""
        with open(self.IP_FILE, "w") as fp:
            fp.write(servers)

from decorator import decorator
from fabric.api import execute, parallel, run


@decorator
def all_servers(task, *args, **kwargs):
    test = args[0]
    hosts = test.ip_list_public_dns
    return execute(parallel(task), *args, hosts=hosts, **kwargs)


class Prepare:
    IP_FILE = "../testrunner/ips.txt"
    STACK_NAME = "a-test"

    def make_ssh_ready(self):
        print("Not Implemented.")

    def make_ips_file(self):
        print("Not Implemented.")

    @all_servers
    def set_environment(self):
        run("echo 'export CBFT_ENV_OPTIONS=bleveMaxResultWindow=10000000' >> /opt/couchbase/bin/couchbase-server")

    def prepare(self):
        self.make_ssh_ready()
        self.make_ips_file()
        self.set_environment()

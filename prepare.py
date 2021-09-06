from decorator import decorator
from fabric.api import execute, parallel, settings, sudo


@decorator
def all_servers(task, *args, **kwargs):
    test = args[0]
    hosts = test.ip_list_public_dns
    return execute(parallel(task), *args, hosts=hosts, **kwargs)


class Prepare:
    IP_FILE = "../testrunner/ips.txt"

    def make_ssh_ready(self):
        print("Not Implemented.")

    def make_ips_file(self):
        print("Not Implemented.")

    @all_servers
    def set_environment(self):
        with settings(sudo_user='root'):
            sudo("sed -i 's/export PATH/export PATH\\nexport "
                 "CBFT_ENV_OPTIONS=bleveMaxResultWindow=10000000/g' "
                 "/opt/couchbase/bin/couchbase-server")
            sudo("service couchbase-server restart")

    def prepare(self):
        self.make_ssh_ready()
        self.make_ips_file()
        # TODO: Need to wait for couchbase to finish installing
        # self.set_environment()

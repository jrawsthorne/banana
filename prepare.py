import sys
from aws import AWSPrepare


class Prepare:
    IP_FILE = "../testrunner/ips.txt"
    STACK_NAME = "a-test"

    def __init__(self):
        pass

    def make_ssh_ready(self):
        print "Not Implemented."

    def make_ips_file(self):
        print "Not Implemented."

    def prepare(self):
        self.make_ssh_ready()
        self.make_ips_file()


def prepare_factory(args):
    cloud = args.pop(0)

    if cloud == "AWS":
        return AWSPrepare(*args)

    return Prepare()

if __name__ == "__main__":
    p = prepare_factory(sys.argv)
    p.prepare()

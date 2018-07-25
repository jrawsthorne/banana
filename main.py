import sys
from aws import AWSPrepare


def prepare_factory(args):
    args.pop(0)
    cloud = args.pop(0)

    if cloud == "AWS":
        return AWSPrepare(*args)


if __name__ == "__main__":
    p = prepare_factory(sys.argv)
    p.prepare()

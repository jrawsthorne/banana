import sys
from prepare_aws import AWSPrepare
from prepare_azure import AzurePrepare
from prepare_gcp import GCPPrepare


def prepare_factory(args):
    args.pop(0)
    cloud = args.pop(0)

    if cloud == "AWS":
        return AWSPrepare(*args)
    if cloud == "Azure":
        return AzurePrepare(*args)
    if cloud == "GCP":
        return GCPPrepare(*args)


if __name__ == "__main__":
    p = prepare_factory(sys.argv)
    p.prepare()

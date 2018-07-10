import argparse


class BucketDumpParser(argparse.ArgumentParser):

    def __init__(self):
        super(BucketDumpParser, self).__init__()

    @staticmethod
    def optparse():
        parser = argparse.ArgumentParser()
        parser.add_argument("-q", "--query", metavar="SEARCH-QUERY", dest="searchQuery",
                            help="provide a search query to search open buckets with")
        parser.add_argument("--random-agent", action="store_true", dest="randomAgent",
                            help="Use a random HTTP User-Agent")
        parser.add_argument("--verbose", action="store_true", dest="runVerbose",
                            help="Run in verbose mode")
        return parser.parse_args()
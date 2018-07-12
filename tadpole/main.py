from lib.settings import (
    gather_bucket_links,
    GRAY_HAT_WARFARE_URL,
    download_files,
    LOOT_DIRECTORY,
    DEFAULT_USER_AGENT,
    get_random_agent,
    BANNER,
    HOME,
    search_files,
    check_ip_address,
    spider_bucket,
    DEFAULT_BUCKET_QUERY
)
from lib.cmd import BucketDumpParser
from lib.output import (
    info,
    success,
    fatal,
    error,
    warn
)


def main():
    try:
        opt = BucketDumpParser().optparse()

        print(BANNER)

        if opt.fileSearch is not None:
            discovered_files = search_files(opt.fileSearch, LOOT_DIRECTORY.format(HOME, ""))
            if len(discovered_files) != 0:
                info("a total of {} files matched your search".format(len(discovered_files)))
                for i, f in enumerate(discovered_files, start=1):
                    print("#{}. {}".format(i, f))
            exit(0)

        if opt.verifyProxy:
            try:
                real_address = check_ip_address()
                address_behind_proxy = check_ip_address(proxy=opt.useProxy)
                if real_address["origin"] == address_behind_proxy["origin"]:
                    warn("it appears your proxy is pointing to your local host")
                else:
                    info("it appears that your proxy is running correctly")
            except ValueError:
                error("something went wrong during JSON conversion, unable to verify proxy")

        if opt.getThisBucket is not None:
            info("connecting to specified S3 bucket '{}'".format(opt.getThisBucket))
            spider_bucket(
                opt.getThisBucket, DEFAULT_BUCKET_QUERY, proxy=opt.useProxy, headers=opt.extraHeaders,
                limit=opt.bucketsToPull
            )
            exit(1)

        if opt.searchQuery is None:
            import os

            fatal("must provide a search query with `-q/--query` flag")
            os.system("python tadpole.py --help")
            exit(1)

        info("searching for open s3 buckets with provided query: '{}'".format(opt.searchQuery))
        post_data = "keywords={}".format(opt.searchQuery)
        if opt.randomAgent is not None:
            agent = get_random_agent(debug=opt.runVerbose).strip()
        else:
            agent = DEFAULT_USER_AGENT
        gathered_links = gather_bucket_links(
            GRAY_HAT_WARFARE_URL, opt.searchQuery, post_data=post_data, user_agent=agent, debug=opt.runVerbose,
            proxy=opt.useProxy, extra_headers=opt.extraHeaders, crawl_bucket=opt.spiderFoundBucket,
            download_limit=opt.bucketsToPull
        )
        info("gathered a total of {} files from {} different bucket(s)".format(
            len(gathered_links[0]), len(gathered_links[1]))
        )
        if len(gathered_links[0]) != 0:
            info("downloading all discovered file(s)")
            for f in gathered_links[0]:
                download_files(f, "{}/{}".format(LOOT_DIRECTORY.format(
                    HOME, opt.searchQuery
                ), f.split("/")[2]), debug=opt.runVerbose, proxy=opt.useProxy)
            success("files have been successfully downloaded into: {}".format(LOOT_DIRECTORY.format(HOME, opt.searchQuery)))
        else:
            error("no open buckets discovered with provided query")
    except KeyboardInterrupt:
        error("user quit")
from lib.settings import (
    gather_bucket_links,
    GRAY_HAT_WARFARE_URL,
    download_files,
    LOOT_DIRECTORY,
    DEFAULT_USER_AGENT,
    get_random_agent,
    BANNER
)
from lib.cmd import BucketDumpParser
from lib.output import (
    info,
    success,
    fatal
)


def main():
    opt = BucketDumpParser().optparse()

    print(BANNER)

    if opt.searchQuery is None:
        fatal("must provide a search query with `-q/--query` flag")
        exit(1)

    info("gathering openbucket links with query: {}".format(opt.searchQuery))
    post_data = "keywords={}".format(opt.searchQuery)
    if opt.randomAgent is not None:
        agent = get_random_agent(debug=opt.runVerbose).strip()
    else:
        agent = DEFAULT_USER_AGENT
    gathered_links = gather_bucket_links(
        GRAY_HAT_WARFARE_URL, opt.searchQuery, post_data=post_data, user_agent=agent, debug=opt.runVerbose
    )
    info("gathered a total of {} files from {} different bucket(s)".format(
        len(gathered_links[0]), len(gathered_links[1]))
    )
    info("downloading all discovered file(s)")
    for f in gathered_links[0]:
        download_files(f, "{}/{}".format(LOOT_DIRECTORY, f.split("/")[2]), debug=opt.runVerbose)
    success("files have been successfully downloaded into: {}".format(LOOT_DIRECTORY))

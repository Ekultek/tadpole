import re
import os
import sys
import urllib2
import platform

import requests
from bs4 import BeautifulSoup

import lib.output


VERSION = "0.0.1"
GRAY_HAT_WARFARE_URL = "https://buckets.grayhatwarfare.com/results"
HOME = os.getcwd()
LOOT_DIRECTORY = "{}/loot".format(HOME)
DEFAULT_USER_AGENT = "BucketDump/{} (Language={};Platform={})".format(
    VERSION, sys.version.split(" ")[0], platform.platform().split("-")[0]
)
#  	tADpOlE 	  Aws Download Open buckEts
BANNER = """\033[36m
  _            _____         ____  _ ______ 
 | |     /\   |  __ \       / __ \| |  ____|
 | |_   /  \  | |  | |_ __ | |  | | | |__   
 | __| / /\ \ | |  | | '_ \| |  | | |  __|  
 | |_ / ____ \| |__| | |_) | |__| | | |____ 
  \__/_/    \_\_____/| .__/ \____/|_|______|[][][]
                     | |                    
                     |_|   Aws Download Open buckEt files v({}) 
\033[0m""".format(VERSION)


def gather_bucket_links(url, query, **kwargs):
    user_agent = kwargs.get("user_agent", None)
    extra_headers = kwargs.get("extra_headers", None)
    post_data = kwargs.get("post_data", None)
    debug = kwargs.get("debug", False)

    aws_regex = re.compile(".amazonaws.", re.I)
    found_files = set()
    page_links = set()
    open_buckets = set()

    headers = {
        "Host": "buckets.grayhatwarfare.com",
        "User-Agent": user_agent,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate",
        "Referer": "https://buckets.grayhatwarfare.com/results/{}".format(query),
        "DNT": "1",
        "Connection": "close",
        "Upgrade-Insecure-Requests": "1",
        "Content-Type": "application/x-www-form-urlencoded"
    }

    if extra_headers is not None:
        for header in extra_headers.keys():
            headers[header] = extra_headers[header]

    req = requests.post(url, data=post_data, headers=headers)
    soup = BeautifulSoup(req.content, "html.parser")
    all_links = soup.find_all('a', href=True)
    for link in all_links:
        if "/results/{}".format(query) in link["href"]:
            page_links.add(link["href"])
            if debug:
                lib.output.debug("found page link: {}".format(link["href"]))
    for page in page_links:
        url = url.replace("/results", page)
        req = requests.get(url, headers=headers)
        soup = BeautifulSoup(req.content, "html.parser")
        for link in soup.find_all('a', href=True):
            if aws_regex.search(link["href"]) is not None:
                found_files.add(link["href"])

    for item in found_files:
        open_buckets.add(item.split("/")[2])
    if debug:
        lib.output.debug("done!")
    return found_files, open_buckets


def download_files(url, path, debug=False):
    if not os.path.exists(path):
        os.makedirs(path)
    try:
        file_path = "{}/{}".format(path, url.split("/")[-1])
        downloader = urllib2.urlopen(url)
        if os.path.isfile(file_path):
            file_path = "{}({})".format(file_path, len([f for f in os.listdir(path) if f == file_path.split("/")[-1]]))
        with open(file_path, "a+") as data:
            meta_data = downloader.info()
            file_size = int(meta_data.getheaders("Content-Length")[0])
            lib.output.info("downloading file: {} bytes: {}".format(url.split("/")[-1], file_size))
            file_size_dl = 0
            block_size = 8192
            while True:
                buffered = downloader.read(block_size)
                if not buffered:
                    break
                file_size_dl += len(buffered)
                if debug:
                    lib.output.debug("{} downloaded".format(file_size_dl))
                data.write(buffered)
                status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
                status = status + chr(8) * (len(status) + 1)
                sys.stdout.write("Progress: {}    \r".format(status))
                sys.stdout.flush()
        lib.output.success("file saved to: {}".format(file_path))
    except urllib2.HTTPError:
        lib.output.fatal("unable to download file: {}".format(url.split("/")[-1]))


def get_random_agent(debug=False):
    import random

    with open("{}/etc/user-agents.txt".format(os.getcwd())) as agents:
        user_agent = random.choice(agents.readlines())
        if debug:
            lib.output.debug("grabbed random User-Agent: {}".format(user_agent.strip()))
        return user_agent.strip()
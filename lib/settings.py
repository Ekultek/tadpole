import re
import os
import sys
import platform

import requests
from bs4 import BeautifulSoup

import lib.output


class AccessDeniedByAWS(Exception): pass


VERSION = "0.0.8"
GRAY_HAT_WARFARE_URL = "https://buckets.grayhatwarfare.com/results"
HOME = os.getcwd()
LOOT_DIRECTORY = "{}/loot/{}"
DEFAULT_USER_AGENT = "tADpOlE/{} (Language={};Platform={})".format(
    VERSION, sys.version.split(" ")[0], platform.platform().split("-")[0]
)
#  	tADpOlE 	  Aws Download Open buckEt files
BANNER = """\033[4;31m{spacer}\033[0m\n\033[1;31m  _            _____         ____  _ ______ 
 | |     /\   |  __ \       / __ \| |  ____|
 | |_   /  \  | |  | |_ __ | |  | | | |__   
 | __| / /\ \ | |  | | '_ \| |  | | |  __|  
 | |_ / ____ \| |__| | |_) | |__| | | |____ 
  \__/_/    \_\_____/| .__/ \____/|_|______|[][][]
                     | |                    
                     |_|   \033[4;32m\033[0m\033[4;36mA\033[0m\033[4;32mws \033[0m\033[4;36mD\033[0m\033[4;32mownload \033[0m\033[4;36mO\033[0m\033[4;32mpen buck\033[0m\033[4;36mE\033[0m\033[4;32mt files v({ver})\033[0m
\033[4;31m{spacer}
\033[0m""".format(ver=VERSION, spacer="-" * 66)


def generate_proxy_dict(proxy):
    retval = {"http": proxy, "https": proxy}
    return retval


def gather_bucket_links(url, query, **kwargs):
    user_agent = kwargs.get("user_agent", None)
    extra_headers = kwargs.get("extra_headers", None)
    post_data = kwargs.get("post_data", None)
    debug = kwargs.get("debug", False)
    proxy = kwargs.get("proxy", None)

    aws_regex = re.compile(".amazonaws.", re.I)
    results_regex = re.compile("results", re.I)
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
    if proxy is not None:
        proxy = generate_proxy_dict(proxy)
    else:
        proxy = {}

    req = requests.post(url, data=post_data, headers=headers, proxies=proxy)
    soup = BeautifulSoup(req.content, "html.parser")
    all_links = soup.find_all('a', href=True)
    for link in all_links:
        if results_regex.search(link["href"]) is not None:
            page_links.add(link["href"])
            if debug:
                lib.output.debug("found page link: {}".format(link["href"]))
    for page in page_links:
        if "!/0" not in page:
            if url[-1] == "/":
                url[-1] = ""
            url = url.replace("/results", page)
            req = requests.get(url, headers=headers)
            soup = BeautifulSoup(req.content, "html.parser")
            for link in soup.find_all('a', href=True):
                if aws_regex.search(link["href"]) is not None:
                    found_files.add(link["href"])
            url = url.replace(page, "/results")

    for item in found_files:
        open_buckets.add(item.split("/")[2])
    if debug:
        lib.output.debug("done!")
    return found_files, open_buckets


def download_files(url, path, debug=False, **kwargs):
    proxy = kwargs.get("proxy", None)

    if proxy is not None:
        proxy = generate_proxy_dict(proxy)
    else:
        proxy = {}

    if not os.path.exists(path):
        os.makedirs(path)
    try:
        if debug:
            lib.output.debug("attempting to download file from {}".format(url))
        filename = url.split("/")[-1]
        file_path = "{}/{}".format(path, filename)
        downloader = requests.get(url, stream=True, proxies=proxy)
        if os.path.isfile(file_path):
            amount = 0
            path = file_path.split("/")
            path.pop()
            path = "/".join(path)
            files_in_path = os.listdir(path)
            for f in files_in_path:
                if filename in f:
                    amount += 1
            file_path = "{}({})".format(file_path, amount)
        try:
            content_length = downloader.headers["Content-Length"]
        except Exception:
            lib.output.warn("unable to determine file length for file '{}'".format(filename))
            content_length = 0
        if int(content_length) >= 200000:
            lib.output.warn("large file being downloaded ({}), this could take a minute".format(filename))
        with open(file_path, "a+") as data:
            for chunk in downloader.iter_content(chunk_size=8192):
                if "AccessDenied" in chunk:
                    data.write("ACCESS DENIED")
                    raise AccessDeniedByAWS("access to s3 bucket is denied by AWS")
                if chunk:
                    data.write(chunk)
        if debug:
            lib.output.success("file saved to: {}".format(file_path))
    except AccessDeniedByAWS:
        lib.output.error("unable to download file: {}; access denied".format(url.split("/")[-1]))
    except Exception as e:
        lib.output.fatal("failed to download file due to unknown error: {}".format(str(e)))


def get_random_agent(debug=False):
    import random

    with open("{}/etc/user-agents.txt".format(os.getcwd())) as agents:
        user_agent = random.choice(agents.readlines())
        if debug:
            lib.output.debug("grabbed random User-Agent: {}".format(user_agent.strip()))
        return user_agent.strip()


def search_files(search_string, directory):
    results = []
    searcher = re.compile(search_string, re.I)
    for root, dirs, files in os.walk(directory):
        for name in files:
            if searcher.search(name) is not None:
                results.append(os.path.join(root, name))
    return results

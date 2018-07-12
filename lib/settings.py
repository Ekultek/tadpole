import re
import os
import sys
import platform

import requests
from bs4 import BeautifulSoup

import lib.output


class AccessDeniedByAWS(Exception): pass


class FileMovedException(Exception): pass


class FileExists(Exception): pass


DEFAULT_BUCKET_QUERY = "single_bucket_search"
VERSION = "0.1.2"
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
    try:
        if type(proxy) == str:
            retval = {"http": proxy, "https": proxy}
        elif type(proxy) == dict:
            retval = proxy
        return retval
    except TypeError:
        retval = proxy

    return retval


def check_ip_address(proxy=None):
    if proxy is not None:
        proxy = generate_proxy_dict(proxy)
    else:
        proxy = {}

    url = "http://httpbin.org/ip"
    req = requests.get(url, proxies=proxy)
    data = req.json()
    return data


def gather_bucket_links(url, query, **kwargs):
    user_agent = kwargs.get("user_agent", None)
    extra_headers = kwargs.get("extra_headers", None)
    post_data = kwargs.get("post_data", None)
    debug = kwargs.get("debug", False)
    proxy = kwargs.get("proxy", None)
    crawl_bucket = kwargs.get("crawl_bucket", False)
    download_limit = kwargs.get("download_limit", 300)

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
    for page in sorted(page_links):
        if "!/0" not in page or not page == "/results/!/0":
            if debug:
                lib.output.debug("currently scraping '{}'".format(page))
            if url[-1] == "/":
                url[-1] = ""
            url = url.replace("/results", page)
            req = requests.get(url, headers=headers, proxies=proxy)
            soup = BeautifulSoup(req.content, "html.parser")
            for link in soup.find_all('a', href=True):
                if aws_regex.search(link["href"]) is not None:
                    found_files.add(link["href"])
            url = url.replace(page, "/results")

    for item in found_files:
        bucket_url = item.split("/")[2]
        open_buckets.add(bucket_url)
        if crawl_bucket:
            # gotta leave out the headers or everything gets messed up
            spider_bucket(bucket_url, query, proxy=proxy, debug=debug, limit=download_limit)
            # except Exception:
            #     lib.output.fatal("issue while downloading bucket files, skipping")
    if debug:
        lib.output.debug("done!")
    return found_files, open_buckets


def spider_bucket(bucket, query, proxy=None, headers=None, debug=False, limit=300):
    if "http" not in bucket:
        bucket = "http://{}".format(bucket)

    if proxy is not None:
        proxy = generate_proxy_dict(proxy)
    else:
        proxy = {}

    lib.output.info("swimming upstream to '{}'".format(bucket))
    req = requests.get(bucket, proxies=proxy, headers=headers)
    soup = BeautifulSoup(req.content, "lxml")
    keys = soup.find_all("key")
    if len(keys) == 0:
        lib.output.error("no files in bucket, skipping")
        return
    key_stripper = lambda s: s.strip("<Key>").strip("</Key>")  # dolla dolla bills ya'll
    lib.output.info("found a total of {} file(s) in S3 bucket '{}', downloading a max of {} file(s)".format(
        len(keys), bucket, limit
    ))
    for i, key in enumerate(keys, start=1):
        if i == limit:
            lib.output.warn("hit max download limit, leaving bucket")
            break
        if i == len(keys):
            lib.output.warn("all files downloaded, leaving bucket")
            break

        try:
            key = key_stripper(str(key.text))
        except Exception as e:
            lib.output.error("error while stripping key: {}".format(e))
            continue

        download_url = "{}/{}".format(bucket, key)
        download_path = "{}/{}".format(
            LOOT_DIRECTORY.format(HOME, query),
            bucket.split("/")[2]
        )
        download_files(
            download_url, download_path,
            debug=debug, proxy=proxy
        )


def download_files(url, path, debug=False, **kwargs):
    proxy = kwargs.get("proxy", None)
    download_anyways = kwargs.get("download_anyways", False)

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
            if not download_anyways:
                raise FileExists
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
        if not os.path.isfile(file_path):
            with open(file_path, "a+") as data:
                for chunk in downloader.iter_content(chunk_size=8192):
                    if "AccessDenied" in chunk:
                        os.unlink(file_path)
                        raise AccessDeniedByAWS("access to s3 bucket is denied by AWS")
                    if "NoSuchKey" in chunk:
                        os.unlink(file_path)
                        raise FileMovedException
                    if chunk:
                        data.write(chunk)
            if debug:
                lib.output.success("file saved to: {}".format(file_path))
        else:
            lib.output.warn("file: '{}' already exists, skipping")
    except AccessDeniedByAWS:
        lib.output.error("unable to download file: {}; access denied".format(url.split("/")[-1]))
    except FileMovedException:
        lib.output.warn("file {} has been moved or deleted out of bucket".format(url.split("/")[-1]))
    except FileExists:
        pass
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

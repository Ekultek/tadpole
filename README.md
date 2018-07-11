# TadPole

Tadpole is a script that leverages [GrayHatWarFare]("https://buckets.grayhatwarfare.com") to download files out of open AWS buckets. You provide a search query and tadpole does the rest.

Why the name tadpole? Well:
```bash
     t
     A WS
     D Ownload
     p 
     O Pen
     l 
buck E t
files 
```

# Installation

To install the program you will need `Python2.7` (3.x coming soon); and you will need to install the requirements:
```bash
pip install -r requirements.txt
```
That's all there is to it!

# Usage examples

Running tadpole without a command will drop you into the help menu:

```bash
(bucketdump) TBG-a0216:tadpole admin$ python tadpole.py
------------------------------------------------------------------
  _            _____         ____  _ ______ 
 | |     /\   |  __ \       / __ \| |  ____|
 | |_   /  \  | |  | |_ __ | |  | | | |__   
 | __| / /\ \ | |  | | '_ \| |  | | |  __|  
 | |_ / ____ \| |__| | |_) | |__| | | |____ 
  \__/_/    \_\_____/| .__/ \____/|_|______|[][][]
                     | |                    
                     |_|   Aws Download Open buckEt files v(0.0.7)
------------------------------------------------------------------

[12:20:57][FATAL] must provide a search query with `-q/--query` flag
usage: tadpole.py [-h] [-q SEARCH-QUERY] [--random-agent] [--verbose]
                  [-P PROXY] [-H HEADER=1,HEADER=2,etc..] [-s STRING]

optional arguments:
  -h, --help            show this help message and exit
  -q SEARCH-QUERY, --query SEARCH-QUERY
                        provide a search query to search open buckets with
  --random-agent        Use a random HTTP User-Agent
  --verbose             Run in verbose mode
  -P PROXY, --proxy PROXY
                        Use a proxy for the requests
  -H HEADER=1,HEADER=2,etc.., --headers HEADER=1,HEADER=2,etc..
                        Pass extra headers with your request
  -s STRING, --search STRING
                        Search for a file and output the location of it
(bucketdump) TBG-a0216:tadpole admin$ 
```

In order to perform a search all you have to do is provide a search query using the `-q/--query` flag:

```bash
(bucketdump) TBG-a0216:tadpole admin$ python tadpole.py -q 'test'
------------------------------------------------------------------
  _            _____         ____  _ ______ 
 | |     /\   |  __ \       / __ \| |  ____|
 | |_   /  \  | |  | |_ __ | |  | | | |__   
 | __| / /\ \ | |  | | '_ \| |  | | |  __|  
 | |_ / ____ \| |__| | |_) | |__| | | |____ 
  \__/_/    \_\_____/| .__/ \____/|_|______|[][][]
                     | |                    
                     |_|   Aws Download Open buckEt files v(0.0.7)
------------------------------------------------------------------

[12:21:45][INFO] searching for open s3 buckets with provided query: 'test'
[12:22:41][INFO] gathered a total of 201 files from 28 different bucket(s)
[12:22:41][INFO] downloading all discovered file(s)
[12:22:42][WARNING] large file being downloaded (test-santosh,-kumar-test-santosh-and-singh-test-santosh-60-1481282779.mp4), this could take a minute
[12:22:48][WARNING] large file being downloaded (test-santosh,-kumar-test-santosh-and-singh-test-santosh-158-1481520151.mp4), this could take a minute

...
```

You have the option to run behind a proxy using the `--proxy` flag:

```bash
(bucketdump) TBG-a0216:tadpole admin$ python tadpole.py -q 'test' --proxy socks5://127.0.0.1:9050
```

You also have the option to pass your own headers:

```bash
(bucketdump) TBG-a0216:tadpole admin$ python tadpole.py -q 'test' -H X-Forwarded-For=1,X-Client=127.0.0.1
```

As well as running with a random User-Agent:

```bash
(bucketdump) TBG-a0216:tadpole admin$ python tadpole.py -q --random-agent
```

Tadpole comes complete with a built in search tool to find the files you're looking for (don't mind the credit cards):

```bash
(bucketdump) TBG-a0216:tadpole admin$ python tadpole.py -s 'web'
------------------------------------------------------------------
  _            _____         ____  _ ______ 
 | |     /\   |  __ \       / __ \| |  ____|
 | |_   /  \  | |  | |_ __ | |  | | | |__   
 | __| / /\ \ | |  | | '_ \| |  | | |  __|  
 | |_ / ____ \| |__| | |_) | |__| | | |____ 
  \__/_/    \_\_____/| .__/ \____/|_|______|[][][]
                     | |                    
                     |_|   Aws Download Open buckEt files v(0.0.7)
------------------------------------------------------------------

[12:25:19][INFO] a total of 9 files matched your search
#1. /Users/admin/bin/python/tadpole/loot/classified/cheapclothes.s3-us-west-2.amazonaws.com/cheap-adrianna-papell-deco-crochet-knit-fit-amp-flare-dress-diverse-rewards-of-free-classified-websites-for-college-students-reviews.html
#2. /Users/admin/bin/python/tadpole/loot/government/picsafe.com.s3.amazonaws.com/government-f6a4075a.webp
#3. /Users/admin/bin/python/tadpole/loot/resume/alexjmeyers.s3-us-west-2.amazonaws.com/Alex J Meyers - Resume (Web).pdf
#4. /Users/admin/bin/python/tadpole/loot/credit card/dumpsterfire.s3.us-east-2.amazonaws.com/credit-card-8x.webp
#5. /Users/admin/bin/python/tadpole/loot/credit card/dumpsterfire.s3.us-east-2.amazonaws.com/credit-card-2x.webp
#6. /Users/admin/bin/python/tadpole/loot/credit card/dumpsterfire.s3.us-east-2.amazonaws.com/credit-card-4x.webp
#7. /Users/admin/bin/python/tadpole/loot/credit card/dumpsterfire.s3.us-east-2.amazonaws.com/credit-card-6x.webp
#8. /Users/admin/bin/python/tadpole/loot/credit card/dumpsterfire.s3.us-east-2.amazonaws.com/credit-card-3x.webp
#9. /Users/admin/bin/python/tadpole/loot/credit card/dumpsterfire.s3.us-east-2.amazonaws.com/credit-card.webp
(bucketdump) TBG-a0216:tadpole admin$ 
```

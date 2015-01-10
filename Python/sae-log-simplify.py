#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Su Yan <http://yansu.org>
# @Date:   2014-01-24 08:52:43
# @Last Modified by:   Su Yan
# @Last Modified time: 2014-01-24 09:46:40

import re

f_input = open('access_log', 'r')
f_output = open('access_simple', 'w')

for line in f_input:
    # re.findall(r'(.*) (.*) (.*) (.*) (\[.*\]) (.*) (.*) (.*) (\".*\") (.*) (.*) (\".*\") (\".*\") (.*) (.*)', log)
    log = re.findall(r'.* (.*) .* .* (\[.*\]) .* .* .* (\".*\") (.*) (.*) (\".*\") (\".*\") .* .*', line)   
    log = list(log[0])
    log[1:1] = '-'
    log[1:1] = '-'
    f_output.write(' '.join(log)+'\n')

f_input.close()
f_output.close()


# -*- encoding: utf-8 -*-

import urllib2
import urllib
import json
import base64
import os
import shutil
from lib.data import conf
from git import Repo
import re

str = 'Doe, John: 555-1212  abs, wewrwr: 13546684'

match = re.findall(r'\w+, \w+: \S+', str)

print match


'''
path = "D:/codes/github/GitHack/output/moonsea/mydata"

for parent, dirnames, filenames in os.walk(path):
	for dirname in dirnames:
		print "parent is:" + parent
		print "dirname is" + dirname

	for filename in filenames:
		print "parent is:" + parent
		print "filename is:" + filename
		print "the full name of the file is:" + os.path.join(parent, filename)
# git_url = "https://github.com/moonsea/mydata.git"
#
# repo = Repo.clone_from(git_url, os.path.join(path, 'repo'), branch='master')
# print repo

github_url = "https://api.github.com/repos/moonsea/ecshop/contents/activity.php?ref=master"

# data={'status':'read','rating':3,'tag':'小说'}  # 根据api文档提供的参数，我们来获取一下阿北读过的书中，他标记了‘小说’这个标签的三星书籍，把这些参数值存在一个dict里

# data = urllib.urlencode(data) # 把参数进行编码

url = urllib2.Request(github_url)

response = urllib2.urlopen(url)

result = json.loads(response.read())

for key in result.keys():
	print key,':',result[key]

a = result['content']
print base64.b64decode(a)
'''

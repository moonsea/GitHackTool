#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import re
import os
import json
import base64
# import urllib
import urllib2
# import shutil
from git import Repo
from lib.data import conf
from lib.data import kb
from subprocess import call

"""
 Request Github API
"""


class Repos(object):

    def __init__(self):
        super(Repos, self).__init__()
        self.base_url = 'https://api.github.com/repos'

    """
    API URL: https://api.github.com/repos/moonsea/ecshop
    """

    def base_info(self):
        super(Repos, self).__init__()
        base_url = '/'.join([self.base_url, conf.user, conf.repo])
        response = self.repo_request(base_url)
        return response

    """
    Clone contents from Github
    """

    def repo_clone(self):
        super(Repos, self).__init__()

        clone_path = os.path.join(conf.output_path, conf.repo)

        if(os.path.isdir(clone_path)):
            str = raw_input(
                "[!] Repo already exists, still reload? Y/n(default n):")
            if (str != 'Y' and str != 'y'):
                return clone_path
            else:
                # shutil.rmtree(clone_path)
                call("rm -rf " + clone_path, shell=True)

        clone_url = kb.base_info['clone_url']

        print "[+] Starting clone repo...."
        Repo.clone_from(clone_url, os.path.join(
            conf.output_path, conf.repo), branch='master')

        return clone_path

    """
    " Return repo content or content list
    """

    def repo_request(self, con_path):
        super(Repos, self).__init__()
        url = urllib2.Request(con_path)
        response = json.loads(urllib2.urlopen(url).read())

        return response

    """
    Traverse repo contents online
    """

    def repo_con_online(self, con_path):

        response = self.repo_request(con_path)

        if(isinstance(response, dict)):
            file_con_en = response['content']
            self.detect_con(file_con_en)  # Detect content
            return

        for item in response:
            print item['name'], '---', item['path']
            # if(item.has_key('content')):
            #     file_con_en = dic['content']
            #     self.detect_con(file_con_en) # Detect content
            #     return
            # else:
            self.repo_con(item['url'])

    """
    Traverse repo contents offline
    """

    def repo_con_offline(self, repo_clone_path):
        super(Repos, self).__init__()

        for parent, dirnames, filenames in os.walk(repo_clone_path):
            # Ignore Directories #
            dirnames[:] = list(set(dirnames).difference(set(conf.ignore_dir)))

            for filename in filenames:
                if(self.detect_file_type(filename)):
                    file_path = os.path.join(parent, filename)
                    self.detect_file_con(file_path)

    """
    Detect file type according to conf.ignore_type
    """

    def detect_file_type(self, filename):
        file_type = filename.split('.')
        if(len(file_type) > 1):
            return file_type[-1] not in conf.ignore_type
        else:
            return True

    """
    Open file, then to call detect_con function
    """

    def detect_file_con(self, file_path):
        super(Repos, self).__init__()

        file_object = open(file_path)
        try:
            lines = file_object.readlines()
            self.detect_con(lines, file_path, 'offline')
        finally:
            file_object.close()

    """
    " Detect Content
    " Input: file encoded content
    """

    def detect_con(self, file_con, file_path, con_type):
        super(Repos, self).__init__()

        # Decode online file content and split content to lines #
        if(con_type == 'online'):
            file_con = base64.b64decode(con_type)
            file_con = file_con.split('\n')

        for line in file_con:
            # IP #
            match_ip = self.detect_ip(line)

            if(match_ip):
                conf.count += 1
                print '[num]:', conf.count
                print ''
                # print '[path]:', file_path

    ##
    # Detect IP
    ##
    def detect_ip(self, line):
        match = re.search(conf.sense_ip, line)

        if(match):
            match_con = match.group()

            if(match_con in conf.ignore_ip):
                return False

            begin_index = line.index(match_con)
            if(begin_index > 0):
                str = line[begin_index - 1]
                if(str.isdigit() or str in conf.ignore_ip_prefix):
                    return False

            end_index = begin_index + len(match_con)
            if(end_index <= len(line)):
                str = line[end_index]
                if(str.isdigit() or str in conf.ignore_ip_suffix):
                    return False

            print '[line]:', line.strip()
            print '[group]:', match_con

            return True
        return False

    """
    " Return repo content with leaked information
    " root content api url: https://api.github.com/repos/moonsea/ecshop/contents
    " normal content api url: https://api.github.com/repos/moonsea/ecshop/contents/admin?ref=master"
    """

    def repo_leak_con(self):
        super(Repos, self).__init__()
        # root_con_path_online = '/'.join([self.base_url, conf.user, conf.repo, 'contents'])

        " Clone Repo Contents to Local Disk "
        conf.repo_clone_path = self.repo_clone()

        " Analyse Repo contents "
        print "[+] Starting analysing repo ..."
        self.repo_con_offline(conf.repo_clone_path)

        '''
        " Root Content "
        root_con = self.repo_request(root_con_path_online)
        '''

        return

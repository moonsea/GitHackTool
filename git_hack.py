#!/usr/bin/env python
# -*- encoding: utf-8 -*-

import sys
import os
import urlparse
from lib.repos import Repos
from lib.data import conf
from lib.data import kb

if len(sys.argv) == 1:
    msg = """

Github disclosure exploit. By moonsea

Usage: python git_hack.py https://github.com/user/repo

"""
    print msg
    sys.exit(0)


def init():
    conf.repo_url = sys.argv[-1]
    # conf.domain = urlparse.urlparse(sys.argv[-1]).netloc.replace(':', '_')
    repo_path = urlparse.urlparse(sys.argv[-1]).path.split('/')
    conf.user = repo_path[1]
    conf.repo = repo_path[2]
    conf.repo = conf.repo if conf.repo[-4:] != '.git' else conf.repo[:-4]
    conf.output_path = os.path.join('output', conf.user)

    """
    Create Output Directory
    /output/user
    """
    if not os.path.exists(conf.output_path):
        os.makedirs(conf.output_path)


def repo():
    repos = Repos()

    """
    " Basic info
    " username
    " owner
    " - login
    " description
    " contents_url
    " language
    " stargazers_count
    " watchers_count
    " clone_url
    """
    kb.base_info = repos.base_info()

    """
    " Repo Content List - Root
    " name
    " path
    " size
    " url
    " html_url
    " download_url
    " type
    """
    kb.repo_leak_con = repos.repo_leak_con()


def main():
    init()
    repo()

if __name__ == '__main__':
    main()

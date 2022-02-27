#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""

   File Name   :   utils.py
   author      :   zhuxiaofei@corp.netease.com
   Date：      :   2022-02-26
   Description :

"""
import logging
import subprocess
import traceback

from urllib.parse import urlparse

import yaml

CFG_PATH = '/Users/zhuxiaofei/PycharmProjects/blog/hexo/_config.yml'
THEME_DIR = "/Users/zhuxiaofei/PycharmProjects/blog/hexo/themes/"


def read_yml(file_path) -> dict:
    """

    :param file_path:
    :return:
    """
    config_map = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        config_map = yaml.safe_load(f)

    return config_map


def save_yml(file_path, content) -> bool:
    """

    :param file_path:
    :param content:
    :return:
    """
    with open(file_path, 'w+', encoding='utf-8') as f:
        content = yaml.safe_dump(content)
        f.write(content)

    return True


def chg_cfg_props(file_path, key, value) -> str:
    cfg_map = read_yml(file_path)
    cfg_map[key] = value
    res = save_yml(file_path, cfg_map)
    return value


#
# config = read_yml(_config_file_path)
# res = save_yml('./test.yml', config)
# print('fff')
def project_init():
    chg_cfg_props(CFG_PATH, 'title', 'title')
    chg_cfg_props(CFG_PATH, 'author', 'author')
    chg_cfg_props(CFG_PATH, 'subtitle', 'subtitle')
    chg_cfg_props(CFG_PATH, 'description', 'description')


def exec_command(cmd):
    """
    执行一个命令
    :param cmd: a list of params
    :return:
    """
    try:
        child = subprocess.Popen(
            cmd,
            stderr=subprocess.PIPE,
            stdout=subprocess.PIPE,
            cwd=THEME_DIR
        )
        out, err = child.communicate()
        child.wait(timeout=60)
        if out or err:
            logging.info("exec error: %s" % err.decode('utf-8'))
        result = out or err.decode('utf-8')
    except Exception as ex:
        logging.error(ex)
        logging.error(traceback.format_exc())
        result = None

    return result


def git_clone(git_url):
    """
    从git url克隆代码
    :param git_url:
    :return:
    """
    p = urlparse(git_url).path.split('/')[-1].replace('.git', '')
    cmd = ['git', 'clone', git_url]
    res = exec_command(cmd)
    if res is None:
        return 'error'
    return 'success'


# project_init()
git_clone("https://github.com/litten/hexo-theme-yilia.git")

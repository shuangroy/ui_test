#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
 @desc:读取配置文件
 @author: nancy
"""
import os
import sys
import configparser
import codecs

conf_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/config/config.ini'
print(conf_path)


class ReadConfig:
    """
    专门读取配置文件的，.ini文件格式
    """

    def __init__(self, filename=conf_path):
        # configpath = filename
        # with open(filename, 'r', encoding='UTF-8') as f:
        #     # f = open(configpath, encoding='UTF-8')
        #     data = f.read()
        #     # remove BOM
        #     if data[:3] == codecs.BOM_UTF8:
        #         data = data[3:]
        #         files = codecs.open(filename, "w")
        #         files.write(data)
        #         files.close()
        # fd.close()

        self.cf = configparser.ConfigParser()
        self.cf.read(filename, encoding='UTF-8')  # read(file_path, encoding='UTF-8'), 如果代码有中文注释，用这个，不然报解码错误

    def getValue(self, env, name):
        """读取配置文件中的值"""
        return self.cf.get(env, name)


if __name__ == '__main__':
    # read = ReadConfig()
    # browser = read.getValue("browserType", "browserName")
    # print(browser)
    pass

#!/usr/bin/env python
#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        模块1
# Purpose:
#
# Author:      yangjun03
#
# Created:     03/02/2015
# Copyright:   (c) yangjun03 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import urllib2
import linecache
import re

from cmdLib import *

#直接读取远程ftp文件到内存, 可以根据regExp进行初步过滤
def geFtpFile2Memory(ftpPath, regExp):
    try:
        #fp = urllib2.urlopen("ftp://yf-tuangou-new-web00.yf01/home/tuan/odp/log/zhixin/zhixin.log.2015020315")
        fp = urllib2.urlopen(ftpPath)
        line_list = []
        for line in fp:
            line = line.strip()
            pattern = re.compile(regExp)
            match = pattern.search(line)
            if match:
                line_list.append(line)
        return line_list
    except Exception as e:
        raise Exception("geFtpFile2Memory ERROR")

#读取远程ftp文件得到文件指针
def geFtpFile(ftpPath):
    #fp = urllib2.urlopen("ftp://yf-tuangou-new-web00.yf01/home/tuan/odp/log/zhixin/zhixin.log.2015020315")
    fp = urllib2.urlopen(ftpPath)
    return fp

def downFtpFile(filePath, dstFilePath):
    #cmdstr = "wget -O zhixin.log.2015020315---yf-tuangou-new-web00.yf01 ftp://yf-tuangou-new-web00.yf01/home/tuan/odp/log/zhixin/zhixin.log.2015020315"
    cmdstr = "wget -O " + dstFilePath + " " + filePath
    status,output=cmd_execute(cmdstr)
    print status,output

if __name__ == '__main__':
    ftpPath = "ftp://yf-tuangou-new-web00.yf01/home/tuan/odp/log/zhixin/zhixin.log.2015020315"
    line_list = geFtpFile2Memory(ftpPath, r"zhixin")


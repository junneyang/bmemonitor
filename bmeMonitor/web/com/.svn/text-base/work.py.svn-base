#!/usr/bin/env python
#-*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        模块1
# Purpose:
#
# Author:      yangjun03
#
# Created:     13/02/2015
# Copyright:   (c) yangjun03 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

import multiprocessing

class Worker(multiprocessing.Process):
    def __init__(self, name):
        multiprocessing.Process.__init__(self, name=name)
        self.name = name
    def run(self):
        print 'In ' + self.name

if __name__ == '__main__':
    jobs = []
    for i in range(5):
        p = Worker(str(i))
        jobs.append(p)
        p.start()
    for j in jobs:
        j.join()

#-------------------------------------------------------------------------------
# Name:        Ä£¿é1
# Purpose:
#
# Author:      yangjun03
#
# Created:     09/02/2015
# Copyright:   (c) yangjun03 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import threading
import time

class testRunner(threading.Thread):
    def __init__(self, name):
        threading.Thread.__init__(self,name=name)
    def run(self):
        print self.name + " started"
        time.sleep(5)
        print self.name + " ended"

def main():
    '''for i in xrange(5):
        th = testRunner(str(i))
        th.start()
        th.join()'''
    th_list = []
    for i in xrange(5):
        th = testRunner(str(i))
        th_list.append(th)
        th.start()
    for th in th_list:
        th.join()


if __name__ == '__main__':
    main()

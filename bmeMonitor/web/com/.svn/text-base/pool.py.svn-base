#-------------------------------------------------------------------------------
# Name:        Ä£¿é1
# Purpose:
#
# Author:      yangjun03
#
# Created:     13/02/2015
# Copyright:   (c) yangjun03 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import time

def main():
    a = [1,2,3,4,5,6,7,8,9]
    limit = 3
    offset = 0
    length = len(a)
    cnt = None
    if(length%limit == 0):
        cnt = length/limit
    else:
        cnt = length/limit + 1
    #print cnt
    for i in xrange(cnt):
        for j in xrange(limit):
            if(i*limit + j + 1 <= length):
                print a[i*limit + j]
        time.sleep(1)
        print "////////////////////////"


if __name__ == '__main__':
    main()

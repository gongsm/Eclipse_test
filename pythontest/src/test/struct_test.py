#-*- coding: UTF-8 -*-
'''
Created on 2015年7月17日

@author: gong_shengmin
'''
import struct
def bmpchk(pic):
    with open(pic,'rb') as p:
        pp = struct.unpack('<ccIIIIIIHH',p.read(30))
        if pp[0] == 'B':
            if pp[1] == 'M':
                print "%s is a windows bitmap" % pic
                print "this bitmap width:%d,height %d coloremode:%d" %(pp[6],pp[7],pp[9])        
            elif pp[1] == 'A':
                print "%s is a OS/2 bitmap" % pic
                print "This bitmap weight:%s high:%s ,and coloreMode is %s!"%(pp[6],pp[7],pp[9])
        else:
            print "This file not a bitmap!"
         
         
         
            
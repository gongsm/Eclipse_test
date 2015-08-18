'''
Created on 30.11.2014

@author: dk

IOM Binary Config Generator for A429
'''

import struct
from bunch import Bunch

from iomGenBinConst import IOM
from iomGenBinEndian import ENDIAN
from stringtab import stringtable

def buildA429InputMessage(x):
    return ""

def buildA429Input(xmlroot):
    messages     = ""
    nummessages  = 0
    
    section = xmlroot.find("A429Input")
    if section is not None:
        for x in section.iterfind("A429Message"):
            messages += buildA429InputMessage(x)
            nummessages += 1

    return Bunch(messages=messages, 
                 messageCount=nummessages, 
                 messageStart=0)

def buildA429OutputMessage(x):
    return ""

def buildA429Output(xmlroot):
    messages     = ""
    nummessages  = 0
    
    section = xmlroot.find("A429Output")
    if section is not None:
        for x in section.iterfind("A429Message"):
            messages += buildA429OutputMessage(x)
            nummessages += 1

    return Bunch(messages=messages, 
                 messageCount=nummessages, 
                 messageStart=0)
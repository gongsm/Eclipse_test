'''
Created on 30.11.2014

@author: dk

IOM Binary Config Generator for CAN
'''

from bunch import Bunch
import struct

from iomGenBinConst import IOM
from iomGenBinEndian import ENDIAN
from stringtab import stringtable

# --------------------------------------------------------------
# CAN Input: 
# --------------------------------------------------------------

encoding_table = {
    ("INT",   1,   "INT"):   IOM.SIGINTYPE_INT8,
    ("INT",   2,   "INT"):   IOM.SIGINTYPE_INT16,
    ("INT",   4,   "INT"):   IOM.SIGINTYPE_SIG32,

    ("UINT",  1,  "INT"):    IOM.SIGINTYPE_UINT8,
    ("UINT",  2,  "INT"):    IOM.SIGINTYPE_UINT16,
    ("UINT",  4,  "INT"):    IOM.SIGINTYPE_SIG32,

    ("FLOAT", 4, "FLOAT"):   IOM.SIGINTYPE_SIG32,

    ("BOOL",  4, "BOOL"):    IOM.SIGINTYPE_BOOL,
    ("BOOL",  4, "INT"):     IOM.SIGINTYPE_CODED32,
    ("COD",   4, "ENUM"):    IOM.SIGINTYPE_CODED32,
    ("COD",   4, "INT"):     IOM.SIGINTYPE_CODED32,
    ("COD",   8, "ENUM"):    IOM.SIGINTYPE_CODED64,
    ("COD",   8, "INT"):     IOM.SIGINTYPE_CODED64,
    ("BYTES", 1, "OPAQUE"):  IOM.SIGINTYPE_OPAQUE, 
    ("INT",   1,   "COUNT"): IOM.SIGINTYPE_INT8_ADD,
}


def buildCanInputParam(xpar):

    paramNameValue  = xpar.attrib["paramNameValue"]
    paramNameStatus = xpar.attrib["paramNameStatus"]
    paramType       = xpar.attrib["paramType"]

    param = struct.pack(ENDIAN + "iihhii",
        int(xpar.attrib["paramOffsetValue"]),
        int(xpar.attrib["paramOffsetStatus"]),
        1, 0,
        stringtable.append(paramNameValue),
        stringtable.append(paramNameStatus),
    )        

    x = xpar.find('source')

    sigtype   = x.attrib["type"]
    access    = int(x.attrib["access"])
    byteoffset = int(x.attrib["offset"])
    bitlen     = int(x.attrib["bits"])
    lsb        = int(x.attrib["lsb"])
    scale      = float(x.attrib["lsbvalue"])
    
    key = (sigtype, access, paramType)
    encoding   = encoding_table.get(key)

    if encoding is None:
        raise Exception, "Bad parameter-signal type combination for %s: %s" % (paramNameValue, str(key))

    signal = struct.pack(ENDIAN + "Iihhf", byteoffset, bitlen, lsb, encoding, scale)

    return param + signal

def buildCanInputMessage(xmsg):
    mappings = ""
    count = 0
    
    for xpar in xmsg.iterfind("Parameter"):
        mappings += buildCanInputParam(xpar)
        count += 1

    header = struct.pack(ENDIAN + "iIihbb", 
        int(xmsg.attrib["id"]),
        int(xmsg.attrib["canId"]),
        int(xmsg.attrib["rate"]),
        16 + len(mappings),         # size of structure plus mappings 
        int(xmsg.attrib["length"]),
        count
    )
    
    return header + mappings

def buildCanInput(endianess, xmlroot):
    
    global ENDIAN
    ENDIAN = endianess
    
    # initialize objects build here global variables
    messages     = ""
    nummessages  = 0
    
    section = xmlroot.find("CanInput")
    if section is not None:
        for x in section.iterfind("CanMessage"):
            messages += buildCanInputMessage(x)
            nummessages += 1

    return Bunch(messages=messages, 
                 messageCount=nummessages, 
                 messageStart=0)

# --------------------------------------------------------------
# CAN Output: Not yet implemented
# --------------------------------------------------------------
def buildCanOutputMessage(x):
    raise Exception, "CAN Output not implemented"
    return ""

def buildCanOutput(endianess, xmlroot):
    global ENDIAN
    ENDIAN = endianess
    
    messages     = ""
    nummessages  = 0
    
    section = xmlroot.find("CanOutput")
    if section is not None:
        for x in section.iterfind("CanMessage"):
            messages += buildCanOutputMessage(x)
            nummessages += 1

    return Bunch(messages=messages, 
                 messageCount=nummessages, 
                 messageStart=0)

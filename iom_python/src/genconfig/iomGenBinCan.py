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

encoding_table_input = {
    ("INT",   1,   "INT"):   IOM.SIGINTYPE_INT8,
    ("INT",   2,   "INT"):   IOM.SIGINTYPE_INT16,
    ("INT",   4,   "INT"):   IOM.SIGINTYPE_INT32,

    ("UINT",  1,  "INT"):    IOM.SIGINTYPE_UINT8,
    ("UINT",  2,  "INT"):    IOM.SIGINTYPE_UINT16,
    ("UINT",  4,  "INT"):    IOM.SIGINTYPE_UINT32,

    ("FLOAT", 4, "FLOAT"):   IOM.SIGINTYPE_FLOATS,

    ("BOOL",  4, "BOOL"):    IOM.SIGINTYPE_BOOL,
    ("BOOL",  4, "INT"):     IOM.SIGINTYPE_CODED32,
    ("COD",   4, "ENUM"):    IOM.SIGINTYPE_CODED32,
    ("COD",   4, "INT"):     IOM.SIGINTYPE_CODED32,
    ("COD",   8, "ENUM"):    IOM.SIGINTYPE_CODED64,
    ("COD",   8, "INT"):     IOM.SIGINTYPE_CODED64,
    ("BYTES", 1, "OPAQUE"):  IOM.SIGINTYPE_OPAQUE, 
    ("INT",   1, "COUNT"):   IOM.SIGINTYPE_INT8_ADD,
}

encoding_table_output = {
        ('INT',   1, 'INT'):    IOM.SIGOUTTYPE_BITFIELD32,
        ('UINT',  1, 'INT'):    IOM.SIGOUTTYPE_BITFIELD32,
        ('INT',   2, 'INT'):    IOM.SIGOUTTYPE_BITFIELD32,
        ('UINT',  2, 'INT'):    IOM.SIGOUTTYPE_BITFIELD32,
        ('INT',   4, 'INT'):    IOM.SIGOUTTYPE_SIG32,
        ('UINT',  4, 'INT'):    IOM.SIGOUTTYPE_SIG32,
        ('BOOL',  4, 'BOOL'):   IOM.SIGOUTTYPE_A664_BOOLEAN,
        ('COD',   4, 'ENUM'):   IOM.SIGOUTTYPE_BITFIELD32,
        ('COD',   4, 'INT'):    IOM.SIGOUTTYPE_BITFIELD32,
        ('BYTES', 1, 'BYTES'):  IOM.SIGOUTTYPE_MULTIPLE_BYTES,
}


def buildCanOutputParam(xpar):

    paramNameValue  = xpar.attrib["paramNameValue"]
    paramNameStatus = xpar.attrib["paramNameStatus"]
    paramType       = xpar.attrib["paramType"]


    signal = ""
    count  = 0
    for xdest in xpar.iterfind("destination"):

        sigtype    = xdest.attrib["type"]
        access     = int(xdest.attrib["access"])
        byteoffset = int(xdest.attrib["offset"])
        bitlen     = int(xdest.attrib["bits"])
        lsb        = int(xdest.attrib["lsb"])
        scale      = float(xdest.attrib["lsbvalue"])
        
        if sigtype == "VALIDITY":
            encoding = IOM.SIGOUTTYPE_VALIDITY_STATUS
        else:
            key        = (sigtype, access, paramType)
            encoding   = encoding_table_output.get(key)

        if encoding is None:
            raise Exception, "Bad parameter-signal type combination for %s: %s" % (paramNameValue, str(key))

        signal += struct.pack(ENDIAN + "Iihhf", byteoffset, bitlen, lsb, encoding, scale)
        count  += 1

    param = struct.pack (ENDIAN + "iihhiiLLL",
                            int(xpar.attrib["paramOffsetValue"]),
                            int(xpar.attrib["paramOffsetStatus"]),
                            count,                                 # number of destinations to write to
                            0,                                     # spare 0
                            stringtable.append(paramNameValue),
                            stringtable.append(paramNameStatus),
                            0, 0, 0                                # no min, max or default for output params
                        )        

    if count == 1:
        # Only one destination, add a second dummy destination so all CAN configs are the same size
        signal += struct.pack(ENDIAN + "Iihhf", 0, 0, 0, 0, 0)
        count  += 1

    if count != 2:
        raise Exception, "Bad number of CAN Output destinations (min 1, max 2) %s: %s" % (paramNameValue, str(count))

    return param + signal



def buildCanInputParam(xpar):

    paramNameValue  = xpar.attrib["paramNameValue"]
    paramNameStatus = xpar.attrib["paramNameStatus"]
    paramType       = xpar.attrib["paramType"]

    validity = xpar.find("validity")
    if validity is not None:
        nofInputs = 2
    else:
        nofInputs = 1

    # Get optional min / max / default values
    if paramType == "FLOAT":
        # Get min / max / default values as float, setting default values if they are not present
        minVal = float(xpar.get("paramMin", 0.0))
        maxVal = float(xpar.get("paramMax", IOM.MAX_VALUE_FLOAT32))
        defVal = float(xpar.get("paramDefault", 0.0))

        param = struct.pack (ENDIAN + "iihhiifff",
                                int(xpar.attrib["paramOffsetValue"]),
                                int(xpar.attrib["paramOffsetStatus"]),
                                nofInputs, 0,
                                stringtable.append(paramNameValue),
                                stringtable.append(paramNameStatus),
                                minVal, maxVal, defVal
                            )        
    else:
        # Get min / max / default values as integer, setting default values if they are not present
        minValInt = int(xpar.get("paramMin", 0))
        maxValInt = int(xpar.get("paramMax", IOM.MAX_VALUE_UTINT32))
        defValInt = int(xpar.get("paramDefault", 0))

        param = struct.pack (ENDIAN + "iihhiiLLL",
                                int(xpar.attrib["paramOffsetValue"]),
                                int(xpar.attrib["paramOffsetStatus"]),
                                nofInputs, 0,
                                stringtable.append(paramNameValue),
                                stringtable.append(paramNameStatus),
                                minValInt, maxValInt, defValInt
                            )        


    x = xpar.find('source')

    sigtype    = x.attrib["type"]
    access     = int(x.attrib["access"])
    byteoffset = int(x.attrib["offset"])
    bitlen     = int(x.attrib["bits"])
    lsb        = int(x.attrib["lsb"])
    scale      = float(x.attrib["lsbvalue"])
    
    key        = (sigtype, access, paramType)
    encoding   = encoding_table_input.get(key)

    if encoding is None:
        raise Exception, "Bad parameter-signal type combination for %s: %s" % (paramNameValue, str(key))

    signal = struct.pack(ENDIAN + "Iihhf", byteoffset, bitlen, lsb, encoding, scale)

    validity = xpar.find("validity")
    if validity is not None:
        # NB: always a Boolean
        encoding   = IOM.SIGINTYPE_BOOL
        byteoffset = int(validity.attrib["offset"])
        bitlen     = 1
        lsb        = int(validity.attrib["lsb"])
        scale      = 1.0

        validitySignal = struct.pack(ENDIAN + "Iihhf", byteoffset, bitlen, lsb, encoding, scale)
    else:
        # Validity not used, add a dummy struct
        validitySignal = struct.pack(ENDIAN + "Iihhf", 0, 0, 0, 0, 0.0)

    return param + signal + validitySignal

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
def buildCanOutputMessage(xmsg):
    mappings = ""
    count = 0
    
    for xpar in xmsg.iterfind("Parameter"):
        mappings += buildCanOutputParam(xpar)
        count    += 1

    header = struct.pack(ENDIAN + "iIihbb", 
        int(xmsg.attrib["id"]),
        int(xmsg.attrib["canId"]),
        int(xmsg.attrib["rate"]),
        16 + len(mappings),         # size of structure plus mappings 
        int(xmsg.attrib["length"]),
        count,

    )
    
    return header + mappings

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

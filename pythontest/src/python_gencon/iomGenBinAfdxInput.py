'''
Created on 30.11.2014

@author: dk

IOM Binary Config Generator for AFDX Input
'''

import struct
from bunch import Bunch

from iomGenBinConst import IOM
from iomGenBinEndian import ENDIAN
from stringtab import stringtable

# Utilities
def hex2int(s):
    if s.startswith("0x"):
        return int(s[2:], 16)
    else:
        return int(s)


# At runtime we assume a message buffer with space for all input messages 
# The message buffer has per message:
#         A 32 byte header (used among others to store message freshness
#         The actual message, padded to 32 bytes (for better DMA performance)
#         A 32 additional header used by IMA SCOE 
#         Rounded to multiple of 64
#
#         In IMA we read the message at buffer start +32 and access the parameters starting
#         at buffer start +64
#         In IDU we read the message at buffer start + 64 AND access data at buffer start + 64
#


message_offset = 0          # next offset into message buffer  
message_dict = {}           # dictionary of message with their offset in message buffer

def messageOffset(messageId, msgOffset):
    intMsgId = int(messageId)
    if not message_dict.has_key(intMsgId):
        raise Exception, "Message Id <%s> not found" % messageId
    
    hdroffset = message_dict[intMsgId]
    return hdroffset + IOM.A664_MESSAGE_HEADER_LENGTH + msgOffset

def freshnessOffset(messageId):
    intMsgId = int(messageId)
    if not message_dict.has_key(intMsgId):
        raise Exception, "Message Id <%s> not found" % messageId
    
    hdroffset = message_dict[intMsgId]
    return hdroffset + IOM.A664_MESSAGE_HEADER_FRESHNESS_OFFSET

# 
# Build functions: convert the XML tag into corresponding binary structure
# side effect: build up string table and message dictionary + message offset
#

def buildLogicSource(xmllogic):
    '''
    Build one logicSource config  structure from XML
    '''
    numconditions = 0
    conditions = ""
    condtypes = [0, 0, 0, 0]
    for x in xmllogic.iterfind("condition"):
        t = x.attrib["type"].lower()
        if t == "freshness":
            condtype = IOM.CONDTYPE_FRESHNESS
            offset  = freshnessOffset(x.attrib["message"])
            mask    = 0     # not used
            value1  = 0     # not used
            value2  = 0     # not used
        elif t == "a664fs":
            condtype = IOM.CONDTYPE_A664FS
            offset  = messageOffset(x.attrib["message"], int(x.attrib["offset"]))
            mask    = 0     # not used
            value1  = 0     # not used
            value2  = 0     # not used
        elif t == "maskvalue":
            condtype = IOM.CONDTYPE_MASKVALUE
            offset  = messageOffset(x.attrib["message"], int(x.attrib["offset"]))
            mask    = hex2int(x.attrib["mask"])
            value1  = int(x.attrib["value"])
            value2  = 0     # not used
        elif t == "a429ssm_bnr":
            condtype = IOM.CONDTYPE_A429SSM_BNR
            offset  = messageOffset(x.attrib["message"], int(x.attrib["offset"]))
            mask    = 0     # not used
            value1  = 0     # not used
            value2  = 0     # not used
        elif t == "a429ssm_dis":
            condtype = IOM.CONDTYPE_A429SSM_DIS
            offset  = messageOffset(x.attrib["message"], int(x.attrib["offset"]))
            mask    = 0     # not used
            value1  = 0     # not used
            value2  = 0     # not used
        elif t == "a429ssm_bcd":
            condtype = IOM.CONDTYPE_A429SSM_BCD
            offset  = messageOffset(x.attrib["message"], int(x.attrib["offset"]))
            mask    = 0    # not used
            value1  = 0    # not used
            value2  = 0    # not used
        else:
            raise Exception, "Illegal condition type: %s" % t
        
        if numconditions > 3:
            raise Exception, "Two many conditions"

        cond = struct.pack(ENDIAN + "IIII", offset, mask, value1, value2)
        condtypes[numconditions] = condtype
        
        conditions += cond
        numconditions += 1
        
    hdr = struct.pack(ENDIAN + "hhbbbb", numconditions, 0, 
                                 condtypes[0], condtypes[1], condtypes[2], condtypes[3])
    return hdr + conditions

encoding_table = {
        ("INT",   4, "INT"):   IOM.SIGINTYPE_SIG32,
        ("UINT",  4, "INT"):   IOM.SIGINTYPE_SIG32,
        ("INT",   4, "FLOAT"): IOM.SIGINTYPE_SIG32_I2F,
        ("INT",   2, "INT"):   IOM.SIGINTYPE_INT16,
        ("UINT",  2, "INT"):   IOM.SIGINTYPE_UINT16,
        ("INT",   1, "INT"):   IOM.SIGINTYPE_INT8,
        ("UINT",  1, "INT"):   IOM.SIGINTYPE_UINT8,
        ("FLOAT", 4, "FLOAT"): IOM.SIGINTYPE_FLOATS,
        ("FLOAT", 4, "INT"):   IOM.SIGINTYPE_SIG32_F2I,
        ("BOOL",  4, "BOOL"):  IOM.SIGINTYPE_BOOL,
        ("BOOL",  4, "INT"):   IOM.SIGINTYPE_CODED32,
        ("COD",   4, "ENUM"):  IOM.SIGINTYPE_CODED32,
        ("COD",   4, "INT"):   IOM.SIGINTYPE_CODED32,
        ("COD",   8, "ENUM"):  IOM.SIGINTYPE_CODED64,
        ("COD",   8, "INT"):   IOM.SIGINTYPE_CODED64,
        ("BNR",   4, "FLOAT"): IOM.SIGINTYPE_BNR,
        ("BNR",   4, "INT"):   IOM.SIGINTYPE_BNR_F2I,
        ("UBNR",  4, "FLOAT"): IOM.SIGINTYPE_BNR,
        ("UBNR",  4, "INT"):   IOM.SIGINTYPE_BNR_F2I,
        ("BCD",   4, "FLOAT"): IOM.SIGINTYPE_BCD,
        ("BCD",   4, "INT"):   IOM.SIGINTYPE_BCD_F2I,
        ("UBCD",  4, "FLOAT"): IOM.SIGINTYPE_BCD,
        ("UBCD",  4, "INT"):   IOM.SIGINTYPE_BCD_F2I,
        ("BYTES", 1, "BYTES"): IOM.SIGINTYPE_OPAQUE,
}

def buildParam(xmlparam, numsources):
    '''
    Build one parameter config structure from XML
    '''
    paramsources = 0
    param = ""
    paramType = xmlparam.attrib['paramType']
    paramName = xmlparam.attrib['paramNameValue']

    for x in xmlparam.iterfind("source"):
        sigType    = x.attrib["type"]
        sigAccess  = int(x.attrib["access"])
        byteoffset = messageOffset(x.attrib["message"], int(x.attrib["offset"]))
        bitlen     = int(x.attrib["bits"])
        lsb        = int(x.attrib["lsb"])
        scale      = float(x.attrib["lsbvalue"])
    
        key = (sigType, sigAccess, paramType)
        encoding   = encoding_table.get(key)

        if encoding is None:
            raise Exception, "Bad parameter-signal type combination for %s: %s" % (paramName, str(key))
            
        source = struct.pack(ENDIAN + "Iihhf", byteoffset, bitlen, lsb, encoding, scale)
        paramsources += 1
        param += source

    if paramsources != numsources:
        raise Exception, "Number of sources mismatch: Logic:%d Parameter:%d" % (numsources, paramsources)
    
    valueOffset      = int(xmlparam.attrib["paramOffsetValue"])
    statusOffset     = int(xmlparam.attrib["paramOffsetStatus"])
    valueNameOffset  = stringtable.append(xmlparam.attrib["paramNameValue"])
    statusNameOffset = stringtable.append(xmlparam.attrib["paramNameStatus"])
    
    hdr = struct.pack(ENDIAN + "iihhii", valueOffset, statusOffset, paramsources, 0, valueNameOffset, statusNameOffset)
    return hdr + param 

def buildAfdxInputDataset(xmlds):
    '''
    Build one data set config structure from XML to binary
    '''
    numsources = 0
    logic = ""
    for x in xmlds.iterfind("Logic/sourceLogic"):
        logic += buildLogicSource(x)
        numsources += 1

    numparams = 0
    param = ""
    for x in xmlds.iterfind("Parameter"):
        param += buildParam(x, numsources)
        numparams += 1

    dslen = 12 + len(logic) + len(param)
    
    hdr = struct.pack(ENDIAN + "hhii", numsources, numparams, len(logic), dslen)
    return hdr + logic + param 



def buildAfdxInputMessage(xmlmsg):
    '''
    Fill the structure
        UInt32_t messageId;           // Message ID from XML Configuration
        UInt32_t messageLength;       // Length of message payload (what is read from port)
        UInt32_t queueLength;         // Queue Length, 0 for Sampling
        UInt32_t messageRate;         // expected update rate of message in ms
        UInt32_t messageHdrOffset;    // Offset in message buffer
        UInt32_t portId;              // Whatever that is on the platform
        UInt32_t portNameOffset;      // Offset of port Name (or CVT name) into string table
    '''
    
    global message_offset
    global message_dict
    
    msgid  = int(xmlmsg.attrib["id"])
    msglen = int(xmlmsg.attrib["length"])
    porttype = xmlmsg.attrib["portType"]
    if porttype[0] == "Q":
        queuelen = int(xmlmsg.attrib["queueLength"])
    else:
        queuelen = 0

    if message_dict.has_key(msgid):
        raise Exception, "Duplicate message id: %d" % msgid
    
    message_dict[msgid] = message_offset

    out = struct.pack(ENDIAN + "iiiiiii",
                      msgid,
                      msglen,
                      queuelen,
                      int(xmlmsg.attrib["rate"]),
                      message_offset,
                      0,    # FIXME: port id not used by application anymore, remove this field in next version
                            # But by setting this to 0, we can compare the binary config files and there
                            # should be no difference between the different positions
                      stringtable.append(xmlmsg.attrib["portName"]))
    
    # increment message offset: 32 byte header + message length padded to MESSAGE_PADDING bytes
    blocklen = (IOM.A664_MESSAGE_HEADER_LENGTH + ((msglen + IOM.A664_MESSAGE_PADDING - 1) & ~(IOM.A664_MESSAGE_PADDING-1)))
    message_offset += blocklen
    return out

def buildAfdxInput(endianess, xmlroot):

    global ENDIAN
    ENDIAN = endianess
    
    # initialize objects build here global variables
    datasets     = ""
    numdataset   = 0
    messages     = ""
    nummessages  = 0
    global message_dict
    global message_offset
    
    message_dict = {}
    message_offset = 0
    
    section = xmlroot.find("AfdxInput")
    if section is not None:
        for x in section.iterfind("AfdxMessage"):
            messages += buildAfdxInputMessage(x)
            nummessages += 1
            
        for x in section.iterfind("DataSet"):
            datasets += buildAfdxInputDataset(x)
            numdataset += 1

    return Bunch(datasets=datasets, 
                 datasetStart=0, 
                 datasetCount=numdataset, 
                 messages=messages, 
                 messageStart=0, 
                 messageCount=nummessages,
                 messageSize=message_offset)


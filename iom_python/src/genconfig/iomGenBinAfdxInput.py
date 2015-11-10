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

import ctypes

encoding_table = {
        ("INT",   4, "INT"):   IOM.SIGINTYPE_INT32,
        ("UINT",  4, "INT"):   IOM.SIGINTYPE_UINT32,
        ("INT",   4, "FLOAT"): IOM.SIGINTYPE_SIG32_I2F,
        ("INT",   2, "INT"):   IOM.SIGINTYPE_INT16,
        ("UINT",  2, "INT"):   IOM.SIGINTYPE_UINT16,
        ("INT",   1, "INT"):   IOM.SIGINTYPE_INT8,
        ("UINT",  1, "INT"):   IOM.SIGINTYPE_UINT8,
        ("FLOAT", 4, "FLOAT"): IOM.SIGINTYPE_FLOATS,
        ("FLOAT", 8, "FLOAT"): IOM.SIGINTYPE_DOUBLE,
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



def GetSelectionSet(xmlds, expectedSetName):
    '''
    '''
    setFound = -1
    numSets  = 0

    #get total number of sources
    for x in xmlds.iterfind("SelectionSet"):

        setName = x.attrib["selectionSetName"]

        if setName == expectedSetName:
            setFound = numSets

        numSets += 1

    if setFound < 0:
        raise Exception, "Set Name not found in list of source sets: %s" % (expectedSetName)

    return setFound 


	
# 
# Build functions: convert the XML tag into corresponding binary structure
# side effect: build up string table and message dictionary + message offset
#

def buildLogicSource(xmllogic, setNumber):
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
            offset   = freshnessOffset(x.attrib["message"])
            sizeBits = 0     # not used
            offBits  = 0     # not used
            value    = 0     # not used
        elif t == "a664fs":
            condtype = IOM.CONDTYPE_A664FS
            offset   = messageOffset(x.attrib["message"], int(x.attrib["offset"]))
            sizeBits = 0     # not used
            offBits  = 0     # not used
            value    = 0     # not used
        elif t == "validityinput":
            condtype = IOM.CONDTYPE_VALIDITY_PARAM
            offset   = messageOffset(x.attrib["message"], int(x.attrib["offset"]))
            sizeBits = hex2int(x.attrib["bits"])
            offBits  = int(x.attrib["lsb"])
            value    = 0     # not used
        elif t == "a429ssm_bnr":
            condtype = IOM.CONDTYPE_A429SSM_BNR
            offset   = messageOffset(x.attrib["message"], int(x.attrib["offset"]))
            sizeBits = 0     # not used
            offBits  = 0     # not used
            value    = 0     # not used
        elif t == "a429ssm_dis":
            condtype = IOM.CONDTYPE_A429SSM_DIS
            offset   = messageOffset(x.attrib["message"], int(x.attrib["offset"]))
            sizeBits = 0     # not used
            offBits  = 0     # not used
            value    = 0     # not used
        elif t == "a429ssm_bcd":
            condtype = IOM.CONDTYPE_A429SSM_BCD
            offset   = messageOffset(x.attrib["message"], int(x.attrib["offset"]))
            sizeBits = 0    # not used
            offBits  = 0    # not used
            value    = 0    # not used
        else:
            raise Exception, "Illegal condition type: %s" % t
        
        if numconditions > 3:
            raise Exception, "Two many conditions"

        cond = struct.pack(ENDIAN + "IIII", offset, sizeBits, offBits, value)
        condtypes[numconditions] = condtype
        
        conditions += cond
        numconditions += 1

    hdr = struct.pack(ENDIAN + "hhbbbb", numconditions, setNumber, 
                                 condtypes[0], condtypes[1], condtypes[2], condtypes[3])
    return hdr + conditions

def buildParam(xmlparam, numsources):
    '''
    Build one parameter config structure from XML
    '''
    paramsources = 0
    param = ""
    paramType  = xmlparam.attrib['paramType']
    paramName  = xmlparam.attrib['paramNameValue']

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
 
    # Get optional min / max / default values
    if paramType == "FLOAT":
        # Get min / max / default values as 32 bit float
        minVal = -IOM.MAX_VALUE_FLOAT32
        maxVal = IOM.MAX_VALUE_FLOAT32
        defVal = 0.0
        if xmlparam.get("paramMin"):
            minVal = float(xmlparam.attrib["paramMin"])

        if xmlparam.get("paramMax"):
            maxVal = float(xmlparam.attrib["paramMax"])

        if xmlparam.get("paramDefault"):
            defVal = float(xmlparam.attrib["paramDefault"])

        hdr = struct.pack(ENDIAN + "iihhiifff", valueOffset, statusOffset, paramsources, 0, valueNameOffset, statusNameOffset, minVal, maxVal, defVal)
    else:
        # Get min / max / default values as 32 integers
        minValInt = 0
        maxValInt = IOM.MAX_VALUE_UTINT32
        defValInt = 0
        if xmlparam.get("paramMin"):
            minValInt = ctypes.c_ulong(int(xmlparam.attrib["paramMin"])).value

        if xmlparam.get("paramMax"):
            maxValInt = ctypes.c_ulong(int(xmlparam.attrib["paramMax"])).value

        if xmlparam.get("paramDefault"):
            defValInt = ctypes.c_ulong(int(xmlparam.attrib["paramDefault"])).value
        
        hdr = struct.pack(ENDIAN + "iihhiiLLL", valueOffset, statusOffset, paramsources, 0, valueNameOffset, statusNameOffset, minValInt, maxValInt, defValInt)

    return hdr + param 


def buildAfdxInputDataset(xmlds):
    '''
    Build one data set config structure from XML to binary
    '''
    numsources = 0
    setNumber  = 0
    logic      = ""
    
    xmlLogic   = xmlds.find("Logic")
    
    for x in xmlLogic.iterfind("sourceLogic"):
        logic += buildLogicSource(x, setNumber)
        numsources += 1

    numparams = 0
    param = ""
    for x in xmlds.iterfind("Parameter"):
        param += buildParam(x, numsources)
        numparams += 1

    dslen = 12 + len(logic) + len(param)

    hdr = struct.pack(ENDIAN + "hhii", numsources, numparams, len(logic), dslen)
    return hdr + logic + param 

def buildAfdxInputDatasetMultiSource(xmlAfdxInput, xmlds):
    '''
    Build one data set config structure from XML to binary
    '''
    numsources = 0
    logic      = ""

    setNumber  = GetSelectionSet (xmlAfdxInput, xmlds.attrib["selectionSetName"])

    xmlLogic   = xmlds.find("Logic")
    
    for x in xmlLogic.iterfind("sourceLogic"):
        logic += buildLogicSource(x, setNumber)
        numsources += 1

    numparams = 0
    param = ""
    for x in xmlds.iterfind("Parameter"):
        param += buildParam(x, numsources)
        numparams += 1

    dslen = 12 + len(logic) + len(param)

    hdr = struct.pack(ENDIAN + "hhii", numsources, numparams, len(logic), dslen)
    return hdr + logic + param 

def buildSigConfig(xmlparam):
    '''
    Build one parameter config structure from XML
    '''

    paramType  = xmlparam.attrib['paramType']
    xmlInput   = xmlparam.find("input")

    sigType    = xmlInput.attrib["type"]
    sigAccess  = int(xmlInput.attrib["access"])
    byteoffset = messageOffset(xmlInput.attrib["message"], int(xmlInput.attrib["offset"]))
    bitlen     = int(xmlInput.attrib["bits"])
    lsb        = int(xmlInput.attrib["lsb"])
    scale      = float(xmlInput.attrib["lsbvalue"])

    key = (sigType, sigAccess, paramType)
    encoding   = encoding_table.get(key)

    sigConfig = struct.pack(ENDIAN + "Iihhf", byteoffset, bitlen, lsb, encoding, scale)

    return sigConfig 



def buildSource(xmlSource):
    '''
    Build one Source config structure (LicParamConfig_t) from XML to binary

    /* Single Source Configuration */
    typedef struct LicParamConfig_t
    {
        UInt32_t        valueMode;   /* Mode of source value: Exact value, any value  */
        UInt32_t        valueExp;    /* expected value of LIC_PARAMETER               */
        UInt32_t        valOffset;   /* Offset of the Parameter Validity in the Input Parameter Buffer */
        UInt32_t        parOffset;   /* Offset of the Parameter in the Input Parameter Buffer */
        UInt32_t        parType;     /* Type of the Parameter in the Input Parameter Buffer, eg IOEN_INPUT_MAPPING_A664_BOOLEAN */
    } LicParamConfig_t;
    '''

    expectedMode    = 0
    expectedValue   = 0
    expected        = xmlSource.attrib["expectedValue"]
    valueOffset     = int(xmlSource.attrib["paramOffsetValue"])
    statusOffset    = int(xmlSource.attrib["paramOffsetStatus"])
    paramType       = xmlSource.attrib["paramType"]

    if paramType == "BOOL":
        type = IOM.SIGINTYPE_BOOL
    else:
        type = IOM.SIGINTYPE_INT32


    if expected == "Any":
        expectedMode  = IOM.SET_SOURCE_PARAM_VALUE_ANY
        expectedValue = 0
    else:
        expectedMode  = IOM.SET_SOURCE_PARAM_VALUE_EXACT
        expectedValue = int(expected)
    

    hdr = struct.pack(ENDIAN + "LLLLL", expectedMode, expectedValue, statusOffset, valueOffset, type)

    return hdr


def buildAfdxInputSourceSet(xmlss):
    '''
    Build one source set config structure from XML to binary
    {
        UInt32_t nofSources;               /* Number of sources in a source set                                                     */
        UInt32_t criteria;                 /* LIC_PARAMETER or SOURCE_HEALTH_SCORE                                                  */
        UInt32_t sourceHealthMode;         /* Source Health Mode: No Lock, Lock Time, Permanent Lock                                */
        UInt32_t sourceHealthValue;        /* lock time in ms                                                                       */
        UInt32_t sourceParamOffset;        /* Offset (in words) of the first source (SourceParamConfig_t) in this set               */
        UInt32_t sourceParamListSize;      /* Total words of the source list for this set (SetConfig_t + (n * SourceParamConfig_t)) */
    }
   '''

    sources      = ""
    oneSourceSet = ""
    numsources   = 0
    criteria     = xmlss.attrib["criteria"]
    global SOURCE_SET_OFFSET
    SOURCE_SET_OFFSET += IOM.SET_HEADER_SIZE


    if criteria == "LIC_PARAMETER":
        # LIC_PARAMETER

        #get total number of sources
        for x in xmlss.iterfind("source"):
            sources    += buildSource(x)

            numsources += 1

        size = IOM.SET_HEADER_SIZE + len(sources)

        oneSourceSet  = struct.pack(ENDIAN + "LLLLLL", numsources, IOM.SET_SOURCE_LIC_PARAMETER, 0, 0, SOURCE_SET_OFFSET, size)

        oneSourceSet += sources
        SOURCE_SET_OFFSET += len(sources)

    else:
        # SOURCE_HEALTH_SCORE

        intervalString = xmlss.attrib["interval"]

        #get total number of sources
        for x in xmlss.iterfind("source"):
            numsources += 1

        #Check lock interval (millisecs, none, permanent)
        if intervalString == "Permanent":
            interval = 0
            intervalmode = IOM.SET_SOURCE_HEALTH_LOCK_PERMANENT
        else:
            interval = int(intervalString)
            
            if interval == 0:
                intervalmode = IOM.SET_SOURCE_HEALTH_NO_LOCK
            else:
                intervalmode = IOM.SET_SOURCE_HEALTH_LOCK

        oneSourceSet = struct.pack(ENDIAN + "LLLLLL", numsources, IOM.SET_SOURCE_HEALTH_SCORE, intervalmode, interval, 0, IOM.SET_HEADER_SIZE)


    return oneSourceSet



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

    out = struct.pack(ENDIAN + "iiiiii",
                      msgid,
                      msglen,
                      queuelen,
                      int(xmlmsg.attrib["rate"]),
                      message_offset,
                      stringtable.append(xmlmsg.attrib["portName"]))
    
    # increment message offset: 32 byte header + message length padded to MESSAGE_PADDING bytes
    blocklen = (IOM.A664_MESSAGE_HEADER_LENGTH + ((msglen + IOM.A664_MESSAGE_PADDING - 1) & ~(IOM.A664_MESSAGE_PADDING-1)))
    message_offset += blocklen
    return out

def buildAfdxInput(endianess, xmlroot):

    global ENDIAN
    ENDIAN = endianess
    
    # initialize objects build here global variables
    datasets         = ""
    numdataset       = 0
    datasetSource    = ""
    numdatasetSource = 0
    messages         = ""
    nummessages      = 0
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
            selectionSetName = x.attrib["selectionSetName"].lower()
            if selectionSetName != "none":
                datasetSource    += buildAfdxInputDatasetMultiSource(section, x)
                numdatasetSource += 1
            else:
                datasets   += buildAfdxInputDataset(x)
                numdataset += 1

    return Bunch(datasets=datasets, 
                 datasetStart=0, 
                 datasetCount=numdataset, 
                 datasetSource=datasetSource, 
                 datasetSourceStart=0, 
                 datasetSourceCount=numdatasetSource, 
                 messages=messages, 
                 messageStart=0, 
                 messageCount=nummessages,
                 messageSize=message_offset)

def buildSourceSet(endianess, xmlroot, offset):

    global ENDIAN
    global SOURCE_SET_OFFSET
    ENDIAN = endianess
    SOURCE_SET_OFFSET = offset + (2*4)
    
    # initialize objects build here global variables
    sourceSet    = ""
    sourceSets   = ""
    numSourceSet = 0
    
    section = xmlroot.find("AfdxInput")
    if section is not None:
        for x in section.iterfind("SelectionSet"):
            sourceSets   += buildAfdxInputSourceSet(x)
            numSourceSet += 1

    # Set the source set header size and offset
    sourceSetHeader = struct.pack(ENDIAN + "LL", numSourceSet, offset + (2*4))
    sourceSet       = sourceSetHeader + sourceSets


    return Bunch(   sourceSet=sourceSet, 
                    sourceSetStart=0, 
                    sourceSetSize=0)


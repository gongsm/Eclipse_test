
import sys
from imtExcelRW import *
from iomGenBinConst import IOM

paramInputColumns = (
    # header,                         value,                         len
      ("Skip",                        "Skip",                         5),
      ("Parameter",                   "Parameter",                   30),
      ("DataType",                    "DataType",                    10),
      ("DataSize",                    "DataSize",                     6),
      ("DefaultVal",                  "DefaultVal",                  10),
                                                                     
      ("RpName",                      "RpName",                      40),
      ("AlertID",                     "AlertID",                     20),
      ("Pubref",                      "Pubref",                      40),
      ("TxLru",                       "TxLru",                       30),
      ("Message",                     "Message",                     40),
      ("DataSet",                     "DataSet",                     40),
      ("DpName",                      "DpName",                      40),
      ("ValidityCriteria",            "ValidityCriteria",            15),
      ("SelectionSet",                "SelectionSet",                10),      
      ("SourceName",                  "SourceName",                  10),
      ("SelectionOrder",              "SelectionOrder",              10),      
                                                                     
      ("FsbOffset",                   "FsbOffset",                   10),
      ("DSOffset",                    "DSOffset",                    10),
      ("DSSize",                      "DSSize",                      10),
      ("ParameterType",               "ParameterType",               10),
      ("BitOffsetWithinDS",           "BitOffsetWithinDS",           10),
      ("ParameterSize",               "ParameterSize",               10),
      ("LsbRes",                      "LsbRes",                      10),
      ("PublisherFunctionalMinRange", "PublisherFunctionalMinRange", 35),
      ("PublisherFunctionalMaxRange", "PublisherFunctionalMaxRange", 35),
      ("FunctionalMinRange",          "FunctionalMinRange",          25),
      ("FunctionalMaxRange",          "FunctionalMaxRange",          25),
      ("MessageRef",                  "MessageRef",                  40),
      ("Status",                      "Status",                      40),      
      ("ChangeHistory",               "ChangeHistory",               40),      
      ("ICDFix",                      "ICDFix",                      40),      
      ("Comment",                     "Comment",                     40),
)

paramOutputColumns = (
    # header,               value,               len
      ("Skip",              "Skip",               5),
      ("Parameter",         "Parameter",         30),
      ("DataType",          "DataType",          10),
      ("DataSize",          "DataSize",           6),
      ("ConstantVal",       "ConstantVal",       10),
                                                
      ("TxLru",             "TxLru",             30),
      ("Message",           "Message",           40),
      ("DataSet",           "DataSet",           40),
      ("DpName",            "DpName",            40),
                                                
      ("FsbOffset",         "FsbOffset",         10),
      ("DSOffset",          "DSOffset",          10),
      ("DSSize",            "DSSize",            10),
      ("ParameterType",     "ParameterType",     10),
      ("BitOffsetWithinDS", "BitOffsetWithinDS", 10),
      ("ParameterSize",     "ParameterSize",     10),
      ("LsbRes",            "LsbRes",            10),
      ("Consumer",          "Consumer",          40),
      ("Comment",           "Comment",           40),
)

afdxMsgInputColumns = (
    # header,                   value,               width
      ("Skip",                  None,                    5),
      ("TxLru",                 "TxLru",                30),
      ("Message",               "Message",              40),
      ("ProtocolType",          "ProtocolType",         40),
      ("A664MsgMaxLength",      "A664MsgMaxLength",     10),
      ("A653MsgLength",         "A653MsgLength",        10),
      ("PortType",              "PortType",             10),
      ("PortQueueLength",       "PortQueueLength",      10),
      ("TxInterval",            "TxInterval",           10),
      ("A653PortRefreshPeriod", "A653PortRefreshPeriod",10),
      ("MaxAge",                "MaxAge",               10),
      ("RxComPortID",           "RxComPortID",          10),
      ("A653PortName",          "A653PortName",         20),
      ("Vlid",                  "Vlid",                 10),
      ("SubVl",                 "SubVl",                10),
      ("BAG",                   "BAG",                  10),
      ("MTU",                   "MTU",                  10),
      ("Networks",              "Networks",             10),
      ("EdeEnabled",            "EdeEnabled",           10),
      ("EdeSourceId",           "EdeSourceId",          10),
      ("DestIP",                "DestIP",               15),
      ("DestUDP",               "DestUDP",              15),
      ("SourceMAC",             "SourceMAC",            15),
      ("SourceIP",              "SourceIP",             15),
      ("SourceUDP",             "SourceUDP",            10),
      ("UniqueKey",             "UniqueKey",            10),
      ("Status",                "Status",               10),
      ("ChangeHistory",         "ChangeHistory",        10),
      ("ICDFix",                "ICDFix",               10),
      ("Comment",               "Comment",              10),      
)


afdxMsgOutputColumns = (
    # header,                   value,               width
      ("Skip",                  None,                    5),
      ("TxLru",                 "TxLru",                30),
      ("Message",               "Message",              40),
      ("ProtocolType",          "ProtocolType",         40),
      ("A664MsgMaxLength",      "A664MsgMaxLength",     10),
      ("A653MsgLength",         "A653MsgLength",        10),
      ("PortType",              "PortType",             10),
      ("PortQueueLength",       "PortQueueLength",      10),
      ("TxInterval",            "TxInterval",           10),
      ("TxComPortID",           "TxComPortID",          10),      
      ("A653PortName",          "A653PortName",         20),
      ("Vlid",                  "Vlid",                 10),
      ("SubVl",                 "SubVl",                10),
      ("BAG",                   "BAG",                  10),
      ("MTU",                   "MTU",                  10),
      ("Networks",              "Networks",             10),
      ("EdeEnabled",            "EdeEnabled",           10),
      ("EdeSourceId",           "EdeSourceId",          10),
      ("DestIP",                "DestIP",               15),
      ("DestUDP",               "DestUDP",              15),
      ("SourceMAC",             "SourceMAC",            15),
      ("SourceIP",              "SourceIP",             15),
      ("SourceUDP",             "SourceUDP",            10),
      ("UniqueKey",             "UniqueKey",            10),
      ("Status",                "Status",               10),
      ("ChangeHistory",         "ChangeHistory",        10),
      ("ICDFix",                "ICDFix",               10),
      ("Comment",               "Comment",              10),      
)

canMsgColumns = (
    # header,               value,           width
      ("Skip",              None,             5),
      ("TxLru",             "TxLru",         30),
      ("Message",           "Message",       40),
      ("Length",            "Length",        10),
      ("Rate",              "Rate",          10),
      ("CanMsgID",          "CanMsgID",      10),
      ("PhysPort",          "PhysPort",      20),
)

a429LabelsColumns = (
    # header,               value,           width
      ("Skip",              None,             5),
      ("TxLru",             "TxLru",         30),
      ("Message",           "Message",       40),
      ("Rate",              "Rate",          10),
      ("Label",             "Label",         10),
      ("PhysPort",          "PhysPort",      20),
)

sourcesColumns = (
    # header,               value,           width
    ("Consumer",           "Consumer",          10),   
    ("DestinationLRUs",    "DestinationLRUs",   10),
    ("SourceName",         "SourceName",        10),
    ("SelectionSet",       "SelectionSet",      10),
    ("SelectionCriteria",  "SelectionCriteria", 10),
    ("SelectionOrder",     "SelectionOrder",    10),
    ("LICParameter",       "LICParameter",      10),
    ("LICValue",           "LICValue",          10),
    ("LockInterval",       "LockInterval",      10),
    ("Comments",           "Comments",          10),
    ("Status",             "Status",            10),
    ("ChangeHistory",      "ChangeHistory",     10),
)

errcount = 0

def logerr(msg):
    global errcount

    sys.stderr.write(msg + "\n")
    sys.stderr.flush()
    errcount+=1

def normalize_datatype(s):
    s = s.lower()
    if s.startswith('int'):
        return 'INT'
    elif s.startswith('count'):
        return 'COUNT'
    elif s == "bitfield":
        return 'INT'
    elif s in ('float', 'real'):
        return "FLOAT"
    elif s.startswith('bool'):
        return "BOOL"
    elif s == 'string':
        return "STRING"
    elif s.startswith('opaq'):
        return "BYTES"
    elif s == "bytes":
        return "BYTES"
    else:
        return ""


def saveIt(outputfn, 
    afdxInputMsgs , canInputMsgs , inputA429Labels , inputSignals,
    afdxOutputMsgs, canOutputMsgs, outputA429Labels, outputSignals,
    sources
):

    genExcelFile(outputfn, 
        (
            ("InputAfdxMessages", afdxMsgInputColumns, 
                sorted(afdxInputMsgs, key=lambda msg: (msg.TxLru, msg.Message)
                )
            ),
            ("InputCanMessages", canMsgColumns, 
                sorted(canInputMsgs, key=lambda msg: (msg.TxLru, msg.Message)
                )
            ),
            ("InputA429Labels", a429LabelsColumns, 
                sorted(inputA429Labels, key=lambda msg: (msg.TxLru, msg.Message)
                )
            ),
            ("InputSignals",  paramInputColumns, 
                sorted(inputSignals, 
                       key=lambda sig: (sig.DataSet, sig.DpName, sig.SelectionOrder, sig.Message)
                )
            ),
            ("OutputAfdxMessages", afdxMsgOutputColumns, 
                sorted(afdxOutputMsgs, key=lambda msg: (msg.TxLru, msg.Message)
                )
            ),
            ("OutputCanMessages", canMsgColumns, 
                sorted(canOutputMsgs, key=lambda msg: (msg.TxLru, msg.Message)
                )
            ),
            ("OutputA429Labels", a429LabelsColumns, 
                sorted(outputA429Labels, key=lambda msg: (msg.TxLru, msg.Message)
                )
            ),
            ("OutputSignals",  paramOutputColumns, 
                sorted(outputSignals, 
                       key=lambda sig: (sig.Message, sig.DataSet, sig.DpName)
                )
            ),
            ("Sources",  sourcesColumns, 
                sorted(sources, 
                       key=lambda src: (src.SelectionSet, src.SelectionOrder)
                )
            ),            
        )
    )


def joinOutputSignals(sigdict, totalparams):
    reclst = []
    existedDp = set()
    for paramrec in totalparams:
        if paramrec.get('Skip') and paramrec.Skip != "" \
           or not paramrec.Parameter \
           or paramrec.DpName in existedDp:
            continue
        existedDp.add(paramrec.DpName)
        rec = Bunch(
            Parameter   = paramrec.Parameter,
            DataType    = normalize_datatype(paramrec.DataType),
            DataSize    = paramrec.DataSize,
            ConstantVal = paramrec.ConstantVal,
            DpName      = paramrec.DpName
        )

        sigrec = sigdict.get(paramrec.DpName)
        if sigrec:
            rec.Skip              = sigrec.Skip
            rec.TxLru             = sigrec.TxLru
            rec.DataSet           = sigrec.DataSet
            rec.Message           = sigrec.Message
            rec.FsbOffset         = sigrec.FsbOffset
            rec.DSOffset          = sigrec.DSOffset
            rec.DSSize            = sigrec.DSSize
            rec.ParameterType     = sigrec.ParameterType
            rec.BitOffsetWithinDS = sigrec.BitOffsetWithinDS
            rec.ParameterSize     = sigrec.ParameterSize
            rec.LsbRes            = sigrec.LsbRes
            rec.Comment           = sigrec.Comment
        else:
            rec.Skip              = "#"
            rec.Lru               = ""
            rec.DataSet           = ""
            rec.Message           = ""
            rec.FsbOffset         = ""
            rec.DSOffset          = ""
            rec.DSSize            = ""
            rec.ParameterType     = ""
            rec.BitOffsetWithinDS = ""
            rec.ParameterSize     = ""
            rec.LsbRes            = ""
            rec.Consumer          = ""
            rec.Comment           = ""

        reclst.append(rec)
    return reclst

def expandBracket(RPName):
    prefix,sep,suffixlist=RPName.partition("[")
    if suffixlist != "":        
        suffixlist = suffixlist[:suffixlist.rfind("]")]
        suffixlist, sep, LsbRes   = suffixlist.partition(":")
        suffixlist = suffixlist.split(",")
        return [prefix+suffix for suffix in suffixlist],LsbRes
    else:
        return [prefix],""
    
def joinInputSignals(sigdict, totalparams, sourceDict):
    reclst = []
    existedRp = set()
    for paramrec in totalparams:
        if paramrec.get('Skip') and paramrec.Skip != "" \
           or not paramrec.Parameter : 
            continue

        if paramrec.SourceName != 'None':
            paramSelectionOrder         = sourceDict[paramrec.SourceName].SelectionOrder
            paramSelectionSet           = sourceDict[paramrec.SourceName].SelectionSet
        else:
            paramSelectionOrder         = "N/A"
            paramSelectionSet           = "None"

        #decode SpecialFunction column
        sfAlertID                 = ""
        sfBcdMultiplier           = ""
        sfValidityParamName       = ""
        sfValidityParamValue      = ""
        sfOutputValidityParamName = ""

        if paramrec.get("SpecialFunction"):   # Optional, None if empty, Format: "AlertId(1446)"
            specialFunction        = paramrec.get("SpecialFunction")
            specialFunction        = specialFunction.strip()           # Remove white spaces
            specialFunction        = specialFunction.replace("(",",")  # Replace opening brackets with comma
            specialFunction        = specialFunction.replace(")","")   # Remove closing bracket
            specialFunctionList    = specialFunction.split(",")        # Split into subtrings based on commas
            specialFunctionList[0] = specialFunctionList[0].lower()    # make lowercase

            if specialFunctionList[0] == "alertid":
                #Special Function AlertID(value)
                sfAlertID = specialFunctionList[1]
            elif specialFunctionList[0] == "validityparameter":
                #Special Function ValidityParameter(name, value)
                sfValidityParamName  = specialFunctionList[1]
                sfValidityParamValue = specialFunctionList[2]
            elif specialFunctionList[0] == "outputvalidityparameter":
                #Special Function OutputValidityParameter(name)
                sfOutputValidityParamName  = specialFunctionList[1]
            elif specialFunctionList[0] == "bcdmultiplier":
                #Special Function BcdMultiplier(value)
                sfBcdMultiplier  = specialFunctionList[1]

        rec = Bunch(
            Parameter                   = paramrec.Parameter,
            DataType                    = normalize_datatype(paramrec.DataType),
            DataSize                    = paramrec.DataSize,
            DefaultVal                  = paramrec.DataDefaultVal,
            RpName                      = paramrec.RpName,
            AlertID                     = sfAlertID,
            FunctionalMinRange          = paramrec.DataMinVal,
            FunctionalMaxRange          = paramrec.DataMaxVal,
            SourceName                  = paramrec.SourceName,
            SelectionSet                = paramSelectionSet,            
            SelectionOrder              = paramSelectionOrder,
            ValidityParamName           = sfValidityParamName,
            ValidityParamValue          = sfValidityParamValue,
            OutputValidityParamName     = sfOutputValidityParamName
        )

        #in case a parameter is a concatenation of ICD RPs (denoted in the iolist with the notation RpName_[1,x,..,y],        
        #meaning the parameter is RpName_1+RpName_x+...+RpName_y, we need to compute the parameter lsb and its size:
        totalParamSize = 0
        firstParam     = None
        firstParamLsb  = 0xFFFF
        paramList, LsbRes = expandBracket(paramrec.RpName)
        for paramRpName in paramList:
            sigrec = sigdict.get(paramRpName)
            if sigrec:
                totalParamSize += sigrec.ParameterSize
                if sigrec.BitOffsetWithinDS < firstParamLsb:
                    firstParam = sigrec
                    firstParamLsb = sigrec.BitOffsetWithinDS
        
        if firstParam:
            firstParam.ParameterSize = totalParamSize
            if LsbRes != "":
                firstParam.LsbRes = LsbRes
                            
        sigrec = firstParam
        if sigrec:
            paramMinValue = sigrec.PublisherFunctionalMinRange
            paramMaxValue = sigrec.PublisherFunctionalMaxRange
            #
            #if paramMinValue == None:
            #    if rec.DataType == "BOOL":
            #        paramMinValue = 0
            #    elif rec.DataType == "FLOAT":
            #        paramMinValue = -IOM.MAX_VALUE_FLOAT32
            #    elif rec.DataType == "INT" or rec.DataType == "COUNT":
            #        paramMinValue = IOM.MIN_VALUE_SINT32                
            #    else:
            #        paramMinValue = "N/A"
            #if paramMaxValue == None:
            #    if rec.DataType == "BOOL":
            #        paramMaxValue = 1
            #    elif rec.DataType == "FLOAT":
            #        paramMaxValue = IOM.MAX_VALUE_FLOAT32
            #    elif rec.DataType == "INT" or rec.DataType == "COUNT":
            #        paramMaxValue = IOM.MAX_VALUE_SINT32
            #    else:
            #        paramMaxValue = "N/A"                    
                
            rec.Skip                        = sigrec.Skip
            rec.Pubref                      = sigrec.Pubref
            rec.TxLru                       = sigrec.TxLru
            rec.Message                     = sigrec.Message
            rec.DataSet                     = sigrec.DataSet
            rec.DpName                      = sigrec.DpName
            rec.ValidityCriteria            = sigrec.ValidityCriteria
            rec.FsbOffset                   = sigrec.FsbOffset
            rec.DSOffset                    = sigrec.DSOffset
            rec.DSSize                      = sigrec.DSSize
            rec.ParameterType               = sigrec.ParameterType
            rec.BitOffsetWithinDS           = sigrec.BitOffsetWithinDS
            rec.ParameterSize               = sigrec.ParameterSize
            rec.LsbRes                      = sigrec.LsbRes
            rec.PublisherFunctionalMinRange = paramMinValue
            rec.PublisherFunctionalMaxRange = paramMaxValue
            rec.Comment                     = sigrec.Comment
            rec.MessageRef                  = sigrec.MessageRef
        else:                     
            rec.Skip                        = "#"
            rec.Pubref                      = ""
            rec.TxLru                       = ""
            rec.Message                     = ""
            rec.DataSet                     = ""
            rec.DpName                      = ""
            rec.ValidityCriteria            = ""
            rec.FsbOffset                   = ""
            rec.DSSize                      = ""
            rec.DSOffset                    = ""
            rec.ParameterType               = ""
            rec.BitOffsetWithinDS           = ""
            rec.ParameterSize               = ""
            rec.LsbRes                      = ""
            rec.PublisherFunctionalMinRange = ""
            rec.PublisherFunctionalMaxRange = ""
            rec.Comment                     = ""
            rec.MessageRef                  = "" 
        try:
            selorder = int(paramrec.SselOrder)
        except:
            selorder = 0


        reclst.append(rec)

    return reclst

def joinOutputMessages(messages, signals):
    '''
    Select the subset of messages referred to by signals
    '''
    # put messages into dictionary indexed by Lru/MsgName
    inpMsgdict = dict()
    for m in messages:
        key = m.Message
        inpMsgdict[key] = m
    
    # traverse signals and put referenced message in output dict
    outMsgdict = dict()
    for s in signals:
        if s.Skip == "#":
            continue
        key = s.Message
        if key in inpMsgdict and not key in outMsgdict:
            outMsgdict[key] = inpMsgdict[key]

    return outMsgdict.values()

def joinInputMessages(messages, signals, type):
    '''
    Select the subset of messages referred to by signals
    '''
    # put messages into dictionary indexed by Lru/MsgName
    inpMsgdict = dict()
    for m in messages:
        key = (m.TxLru, m.Message)
        if type == "afdx":
            m.UniqueKey    = m.TxLru+"::"+m.Message
        inpMsgdict[key] = m
    
    # traverse signals and put referenced message in output dict
    outMsgdict = dict()
    for s in signals:
        if s.Skip == "#":
            continue
        key = (s.TxLru, s.Message)
        if key in inpMsgdict and not key in outMsgdict:
            outMsgdict[key] = inpMsgdict[key]

    return outMsgdict.values()
    
        
import glob        
import os        

def main(args):
    # read ICD Excel
    outfn = args[0]
    infn  = args[1]
    mapfiles = []
    for f in args[2:]:
        mapfiles += glob.glob(f)

    # check parameters
    if len(mapfiles) == 0:
        if len(args[2:]) > 0:
            logerr("Can't open map files: %s" % str(args[2:]))
        usage()
        return -1

    if not os.path.exists(infn):
        logerr("Can't open Excel ICD file: %s" % infn )
        usage()
        return -1
    
    for f in mapfiles:
        if not os.path.exists(infn):
            logerr("Can't open map file: %s" % infn )
            usage()
            return -1
    
    # Read Excel HF ICD
    afdxInputMsgs,  canInputMsgs, inputA429Labels, inputSignals, afdxOutputMsgs, canOutputMsgs, outputA429Labels, outputSignals =  \
        readExcelFile(infn, ('InputAfdxMessages' , 'InputCanMessages' , 'InputA429Labels' ,'InputSignals', 
                             'OutputAfdxMessages', 'OutputCanMessages', 'OutputA429Labels', 'OutputSignals'))

    inputParams  = []
    outputParams = []
    sourcesData  = []

    # Read DD-RP Mapping Sheets 
    for f in mapfiles:
        inMap = None
        sheets = readExcelFile(f, ('ICD Input Parameters',))
        if sheets is None:
            sheets = readExcelFile(f, ('ICD Parameters',))

        if sheets is not None:
            inMap = sheets[0]
            inputParams.extend(inMap)
        
        sheets = readExcelFile(f, ('Sources',))
        if sheets is not None:
            srcData = sheets[0]
            sourcesData.extend(srcData)
            
        outMap = None
        sheets = readExcelFile(f, ('ICD Output Parameters',))
        if sheets is not None:
            outMap = sheets[0]
            outputParams.extend(outMap)
        
        if inMap is None and outMap is None:
            logerr("Can't find Parameter Sheets in map file: %s" % f)

    
    if inputParams == [] and outputParams == []:
        logerr("No parameters to join")
        return -1

    # Join input mappings

    # create signal dictionary to speed up join
    sigdict = dict()
    for sig in inputSignals:
        sigdict[sig.RpName] = sig
        
        
    srcdict = dict()
    for src in sourcesData:
        srcdict[src.SourceName] = src        
        
    # now do the join
    newInputSignals    = joinInputSignals(sigdict, inputParams, srcdict)
    newAfdxInputMsgs   = joinInputMessages(afdxInputMsgs, newInputSignals, "afdx")
    newCanInputMsgs    = joinInputMessages(canInputMsgs, newInputSignals, "can")
    newInputA429Labels = joinInputMessages(inputA429Labels, newInputSignals, "a429")

    # Join output mappings

    # create signal dictionary to speed up join
    sigdict = dict()
    for sig in outputSignals:
        sigdict[sig.DpName] = sig
        
    # now do the join
    newOutputSignals    = joinOutputSignals(sigdict, outputParams)
    newAfdxOutputMsgs   = joinOutputMessages(afdxOutputMsgs, newOutputSignals)
    newCanOutputMsgs    = joinOutputMessages(canOutputMsgs, newOutputSignals)
    newOutputA429Labels = joinOutputMessages(inputA429Labels, newOutputSignals)
    
    saveIt(outfn, 
           newAfdxInputMsgs, newCanInputMsgs, newInputA429Labels, newInputSignals, 
           newAfdxOutputMsgs, newCanOutputMsgs, newOutputA429Labels, newOutputSignals,
           sourcesData)

    return 0


def usage():
    sys.stderr.write('Usage: outputfile icdfile mapfiles...\n')

if __name__ == '__main__':
    if len(sys.argv) < 4:
        usage()
        sys.exit(1)
    else:
        sys.exit(main(sys.argv[1:]))
        
    
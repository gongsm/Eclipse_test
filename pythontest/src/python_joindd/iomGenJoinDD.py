#python iomGenJoinDD.py ./DMH.xlsx ./HF_IDUCENTER-icd.xlsx ./dmh_iolist.xlsx


import sys
from imtExcelRW import *
paramInputColumns = (
    # header,         value,                len
      ("Skip",        "Skip",                5),
      ("Parameter",   "Parameter",          30),
      ("DataType",    "DataType",           10),
      ("DataSize",    "DataSize",            6),
      ("DefaultVal",  "DefaultVal",         10),
      
      ("RpName",      "RpName",             40),
      ("AlertID",     "AlertID",            20),
      ("Pubref",      "Pubref",             40),
      ("Lru",         "Lru",                30),
      ("Message",     "Message",            40),
      ("DataSet",     "DataSet",            40),
      ("Signal",      "Signal",             40),
      ("SSEL",        "SSEL",               15),
      ("SselOrder",   "SselOrder",          10),
      ("MaskValidParam", "MaskValidParam",  20),
      ("MaskValidValue", "MaskValidValue",  20),

      ("FsbOffset",   "FsbOffset",          10),
      ("DSOffset",    "DSOffset",           10),
      ("DSSize",      "DSSize",             10),
      ("SigType",     "SigType",            10),
      ("SigOffset",   "SigOffset",          10),
      ("SigSize",     "SigSize",            10),
      ("LsbValue",    "LsbValue",           10),
      ("Comment",     "Comment",            40),
)

paramOutputColumns = (
    # header,         value,                len
      ("Skip",        "Skip",                5),
      ("Parameter",   "Parameter",          30),
      ("DataType",    "DataType",           10),
      ("DataSize",    "DataSize",            6),
      ("ConstantVal",  "ConstantVal",       10),
      
      ("Lru",         "Lru",                30),
      ("Message",     "Message",            40),
      ("DataSet",     "DataSet",            40),
      ("DpName",      "DpName",             40),
      ("Validity",    "Validity",           15),

      ("FsbOffset",   "FsbOffset",          10),
      ("DSOffset",    "DSOffset",           10),
      ("DSSize",      "DSSize",             10),
      ("SigType",     "SigType",            10),
      ("SigOffset",   "SigOffset",          10),
      ("SigSize",     "SigSize",            10),
      ("LsbValue",    "LsbValue",           10),
      ("Consumer",    "Consumer",           40),
      ("Comment",     "Comment",            40),
)

afdxMsgColumns = (
    # header,               value,           width
      ("Skip",              None,             5),
      ("Lru",               "Lru",           30),
      ("Message",           "Message",       40),
      ("Length",            "Length",        10),
      ("RxLength",          "RxLength",      10),
      ("Overhead",          "Overhead",      10),
      ("Type",              "Type",          10),
      ("QueueLength",       "QueueLength",   10),
      ("Rate",              "Rate",          10),
      ("RxRate",            "RxRate",        10),
      ("PortID",            "PortID",        10),
      ("PortName",          "PortName",      20),
      ("Vlid",              "Vlid",          10),
      ("SubVl",             "SubVl",         10),
      ("BAG",               "BAG",           10),
      ("MTU",               "MTU",           10),
      ("EdeEnabled",        "EdeEnabled",    10),
      ("EdeSourceId",       "EdeSourceId",   10),
      ("DestIP",            "DestIP",        15),
      ("DestUDP",           "DestUDP",       15),
      ("SourceMAC",         "SourceMAC",     15),
      ("SourceIP",          "SourceIP",      15),
      ("SourceUDP",         "SourceUDP",     10),
)

canMsgColumns = (
    # header,               value,           width
      ("Skip",              None,             5),
      ("Lru",               "Lru",           30),
      ("Message",           "Message",       40),
      ("Length",            "Length",        10),
      ("Rate",              "Rate",          10),
      ("CanMsgID",          "CanMsgID",      10),
      ("PhysPort",          "PhysPort",      10),
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
    afdxInputMsgs, canInputMsgs, inputSignals,
    afdxOutputMsgs, canOutputMsgs, outputSignals
):
    genExcelFile(outputfn, 
        (
            ("InputAfdxMessages", afdxMsgColumns, 
                sorted(afdxInputMsgs, key=lambda msg: (msg.Lru, msg.Message)
                )
            ),
            ("InputCanMessages", canMsgColumns, 
                sorted(canInputMsgs, key=lambda msg: (msg.Lru, msg.Message)
                )
            ),
            ("InputSignals",  paramInputColumns, 
                sorted(inputSignals, 
                       key=lambda sig: (sig.Message, sig.DataSet, sig.Signal, sig.Lru)
                )
            ),
            ("OutputAfdxMessages", afdxMsgColumns, 
                sorted(afdxOutputMsgs, key=lambda msg: (msg.Lru, msg.Message)
                )
            ),
            ("OutputCanMessages", canMsgColumns, 
                sorted(canOutputMsgs, key=lambda msg: (msg.Lru, msg.Message)
                )
            ),
            ("OutputSignals",  paramOutputColumns, 
                sorted(outputSignals, 
                       key=lambda sig: (sig.Message, sig.DataSet, sig.DpName)
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
            rec.Skip      = sigrec.Skip
            rec.Lru       = sigrec.Lru
            rec.DataSet   = sigrec.DataSet
            rec.Message   = sigrec.Message
            rec.Validity  = sigrec.Validity
            rec.FsbOffset = sigrec.FsbOffset
            rec.DSOffset  = sigrec.DSOffset
            rec.DSSize    = sigrec.DSSize
            rec.SigType   = sigrec.SigType
            rec.SigOffset = sigrec.SigOffset
            rec.SigSize   = sigrec.SigSize
            rec.LsbValue  = sigrec.LsbValue
            rec.Consumer  = sigrec.Comment
            rec.Comment   = sigrec.Comment
        else:
            rec.Skip      = "#"
            rec.Lru       = ""
            rec.DataSet   = ""
            rec.Message   = ""
            rec.Validity  = ""
            rec.FsbOffset = ""
            rec.DSOffset  = ""
            rec.DSSize    = ""
            rec.SigType   = ""
            rec.SigOffset = ""
            rec.SigSize   = ""
            rec.LsbValue  = ""
            rec.Consumer  = ""
            rec.Comment   = ""

        reclst.append(rec)
    return reclst

def joinInputSignals(sigdict, totalparams):
    reclst = []
    existedRp = set()
    for paramrec in totalparams:
        if paramrec.get('Skip') and paramrec.Skip != "" \
           or not paramrec.Parameter \
           or paramrec.RpName in existedRp:
            continue
        existedRp.add(paramrec.RpName)
        rec = Bunch(
            Parameter = paramrec.Parameter,
            DataType  = normalize_datatype(paramrec.DataType),
            DataSize  = paramrec.DataSize,
            DefaultVal= paramrec.DefaultVal,
            RpName    = paramrec.RpName,
            AlertID   = paramrec.get("AlertID", '') # Optional, None if empty
        )
        sigrec = sigdict.get(paramrec.RpName)
        if sigrec:
            rec.Skip      = sigrec.Skip
            rec.Pubref    = sigrec.Pubref
            rec.Lru       = sigrec.Lru
            rec.Message   = sigrec.Message
            rec.DataSet   = sigrec.DataSet
            rec.Signal    = sigrec.Signal
            rec.SSEL      = sigrec.SSEL
            rec.FsbOffset = sigrec.FsbOffset
            rec.DSOffset  = sigrec.DSOffset
            rec.DSSize    = sigrec.DSSize
            rec.SigType   = sigrec.SigType
            rec.SigOffset = sigrec.SigOffset
            rec.SigSize   = sigrec.SigSize
            rec.LsbValue  = sigrec.LsbValue
            rec.Comment   = sigrec.Comment
        else:
            rec.Skip      = "#"
            rec.Pubref    = ""
            rec.Lru       = ""
            rec.Message   = ""
            rec.DataSet   = ""
            rec.Signal    = ""
            rec.SSEL      = ""
            rec.FsbOffset = ""
            rec.DSSize    = ""
            rec.DSOffset  = ""
            rec.SigType   = ""
            rec.SigOffset = ""
            rec.SigSize   = ""
            rec.LsbValue  = ""
            rec.Comment   = ""
   
        try:
            selorder = int(paramrec.SselOrder)
        except:
            selorder = 0

        rec.SselOrder = selorder
        
        if paramrec.MaskValidFlag and paramrec.MaskValidFlag.lower() == "yes":
            rec.MaskValidParam = paramrec.MaskValidParam
            rec.MaskValidValue = paramrec.MaskValidValue
            rec.SSEL += ',MASK'
        else:
            rec.MaskValidParam = ""
            rec.MaskValidValue = ""

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

def joinInputMessages(messages, signals):
    '''
    Select the subset of messages referred to by signals
    '''
    # put messages into dictionary indexed by Lru/MsgName
    inpMsgdict = dict()
    for m in messages:
        key = (m.Lru, m.Message)
        inpMsgdict[key] = m
    
    # traverse signals and put referenced message in output dict
    outMsgdict = dict()
    for s in signals:
        if s.Skip == "#":
            continue
        key = (s.Lru, s.Message)
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
    afdxInputMsgs,  canInputMsgs, inputSignals, afdxOutputMsgs, canOutputMsgs, outputSignals =  \
        readExcelFile(infn, ('InputAfdxMessages', 'InputCanMessages', 'InputSignals', 
                             'OutputAfdxMessages', 'OutputCanMessages', 'OutputSignals'))

    inputParams  = []
    outputParams = []

    # Read DD-RP Mapping Sheets 
    for f in mapfiles:
        inMap = None
        sheets = readExcelFile(f, ('ICD Input Parameters',))
        if sheets is None:
            sheets = readExcelFile(f, ('ICD Parameters',))

        if sheets is not None:
            inMap = sheets[0]
            inputParams.extend(inMap)
        
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
        
    # now do the join
    newInputSignals  = joinInputSignals(sigdict, inputParams)
    newAfdxInputMsgs = joinInputMessages(afdxInputMsgs, newInputSignals)
    newCanInputMsgs  = joinInputMessages(canInputMsgs, newInputSignals)

    # Join output mappings

    # create signal dictionary to speed up join
    sigdict = dict()
    for sig in outputSignals:
        sigdict[sig.DpName] = sig
        
    # now do the join
    newOutputSignals  = joinOutputSignals(sigdict, outputParams)
    newAfdxOutputMsgs = joinOutputMessages(afdxOutputMsgs, newOutputSignals)
    newCanOutputMsgs  = joinOutputMessages(canOutputMsgs, newOutputSignals)
    
    
    saveIt(outfn, 
           newAfdxInputMsgs, newCanInputMsgs, newInputSignals, 
           newAfdxOutputMsgs, newCanOutputMsgs, newOutputSignals)

    return 0


def usage():
    sys.stderr.write('Usage: outputfile icdfile mapfiles...\n')

if __name__ == '__main__':
    if len(sys.argv) < 4:
        usage()
        sys.exit(1)
    else:
        sys.exit(main(sys.argv[1:]))
        
    


from __future__ import print_function
import sys
import os
import datetime
import getopt
from collections import defaultdict

from bunch import Bunch
import logger

from imtXmlReader import icdReadAll 
from imtExcelRW import genExcelFile



# ---------------------------------------------------------------
# - install extended traceback handler to provide
#   all stack variables and their values, and drop
#   into pdb when an exception occurs

from xtraceback import format_exception
import pdb

def excepthook(ex_cls, ex, tb):
    # tblist = format_exception(ex_cls, ex, tb, with_vars=True)
    # print('\n'.join(tblist))
    pdb.post_mortem(tb)
sys.excepthook = excepthook

# ---------------------------------------------------------------
# helper

def _getAttrib(x, attrib, cast=None, default=None):
    '''
    Get value of XML Record attribute attrib, cast it according to cast.
    If not found or cast fails, return default or None.
    '''
    a = x.a.get(attrib)
    if a is None:
        if default is None:
            logger.nerror("Missing attribute %s" % attrib, TYPE=x.tag, NAME=x.a.Name, FILE=x.filename)
        else:
            logger.nerror("Missing attribute %s. Set to default [%s]" % (attrib, default),
                                TYPE=x.tag, NAME=x.a.Name, FILE=x.filename)
            a = default
    else:
        if cast:
            try:
                a = cast(a)
            except:
                if default is None:
                    logger.nerror("Bad value for attribute %s" % attrib, TYPE=x.tag, NAME=x.a.Name, FILE=x.filename)
                else:
                    logger.nerror("Bad value for attribute %s. Replace with default [%s]" % \
                                (attrib, default), TYPE=x.tag, NAME=x.a.Name, FILE=x.filename)
                    a = default
    return a
# ---------------------------------------------------------------

def _getParentMsg(obj, msgtype):
    '''
    Return Msg parent of an object 
    Ascend the parent hierarchy until an A664Message or the tree root is found
    '''
    while obj.parent:
        obj = obj.parent
        if obj.tag == msgtype:
            return obj
    return None

# ---------------------------------------------------------------

def _getSSMType(xdpclass):
    '''
    Return SSM Type applicable for a signal in a A429 Word. For this
    locate SSM and return its Data Format Type
    This is very inefficient code, but its not used in DS anyway.
    '''
    if xdpclass.tag == "A429Word":
        searchin=xdpclass
    else:
        searchin=xdpclass.parent
    for odp in searchin.e.DP:
        if odp.a.Name == "SSM":
            s = odp.a.DataFormatType
            if s.startswith("A429_"):
                return s[5:]
            else:
                return s
    return ''

def _getTopNode(node):
    '''Get the root node of the HF/HA: this is directly under xroot'''
    while node.parent.parent:
        node = node.parent
    return node

def _getDSPath(xdp, msgtype):
    '''Get the path from outmost dataset to a DP'''
    res = xdp.tag
    while xdp.parent:
        xdp = xdp.parent
        res = xdp.tag + '.' + res
        if xdp.tag == msgtype:
            return res
    return None

_a249labeldpnames = frozenset(("LABEL", "SDI", "SSM", "PARITY"))
        
def _getA429SingleDP(xword):
    '''
    Get the single Data DP from a 429 word. 
    If the word has more than one data DP or none at all, return None
    '''
      
    count = 0
    found = None
    for xdp in xword.e.get('DP', []):
        if xdp.a.Name.upper() not in _a249labeldpnames:
            found = xdp
            count += 1
    if count == 1:
        return found
    else:
        return None
    
def _makeMulticastIpAddr(vlid):
    return "224.224.%d.%d" % (vlid / 256, vlid % 256)

# ---------------------------------------------------------------

class IcdProcessor():

    '''
    Process Aviage input model and create an in-core output model
    isomorph to the IMT data model.
    The output IMT model will then be traversed by the save function
    and recursively saved to DB.
    The ouput model is an ad-hoc construct of bunches and lists
    suitable for simple traversal.
    '''

    #
    def __init__(self, xroot):

        self.xroot = xroot                      # root of input model
        self.xindex         = dict()            # cross reference for Guid's
        self.vlxref         = dict()
        self.gwsignalxref   = dict()            # index to find signals from gateways refering to an RP by RP Guid
        self.pubrefxref     = defaultdict(list) # index to find DP by PUBREF
        self.appportXref    = dict()
        self.guidIndex(self.xroot)              # build Guid lookup dictionary

    def reset(self):
        self.rplist         = dict()            # table indexed by RP containing all info per signal for  IOM Generation
        self.rpuniq         = dict()            # table indexed by RP containing all info per signal for  IOM Generation
        self.dplist         = dict()            # table indexed by RP containing all info per signal for  IOM Generation
        self.rxMessagelist  = dict()            # table indexed by msg Name containing all info per message 
        self.txMessagelist  = dict()            # table indexed by msg Name containing all info per message 
        

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    EXCLUDE_FROM_INDEX = set(['Port_Ref'])

    def guidIndex(self, node):
        '''
        Build Guid lookup dictionary
        Parameters:
        - node: tree node to index

        Recursively traverse model tree and gather all Guid's
        in a cross reference dictionary.
        '''
        if not node.tag in IcdProcessor.EXCLUDE_FROM_INDEX:
            guid = node.a.get("Guid")
            if guid:
                if guid in self.xindex:
                    logger.nerror(
                        "IMPORT.GUIDINDEX",
                        "Duplicate Guid",
                        TAG     = node.tag, 
                        GUID    = guid, 
                        OTHER   = self.xindex[guid].tag)
                else:
                    self.xindex[guid] = node

        for nodelist in node.e.values():
            for node in nodelist:
                self.guidIndex(node)
    
    def getClass(self, node):
        return self.xindex[node.a.GuidDef]

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    def recursiveGwLink(self, parent):
        '''
        Recursively traverse tree and gather Gw_Pub_Refs
        '''
        for objtype, objlist in parent.e.items():
            if objtype == "Gw_Pub_Ref":
                for xgw in objlist:
                    self.gwsignalxref[xgw.a.DestGuid] = xgw.parent
            else:
                for obj in objlist:
                    self.recursiveGwLink(obj)
    
                    
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    def makeGatewayReverseMap(self):
        '''
        Traverse all Gateways and build cross ref
        '''
        for xha in self.xroot.e.get('RemoteGateway', []):
            for xport in xha.e.get('HFQueuingPort',[]) + xha.e.get('HFSamplingPort', []) + xha.e.get('CANPort', []):
                if xport.a.Direction != 'Source':
                    continue
                for xmsg in xport.e.get('A664Message', []):
                    for xds in xmsg.e.get('DS', []):
                        self.recursiveGwLink(xds)
                for xmsg in xport.e.get('CANMessage', []):
                    for xds in xmsg.e.get('DP', []):
                        self.recursiveGwLink(xds)
    
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    def checkContainment(self, xinner, xouter):
        '''
        Generic function to check whether xinner is contained by xouter
        '''
        container = xinner.parent
        while container:
            if container == xouter:
                return True
            container = container.parent
        return False
            
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    porttype2msgtype = {
        "HFSamplingPort":   "A664Message",
        "HFQueuingPort":    "A664Message",
        "A653SamplingPort": "A664Message",
        "A653QueuingPort":  "A664Message",
        "CANPort":          "CANMessage",
    }

    def processFunctionRPs(self, hfnamelist):
        '''
        Traverse hosted function/application and process all RP
        '''
        functypes =  ("A653ApplicationComponent", "HostedFunction")
        porttypes =  ("A653SamplingPort", "A653QueuingPort", "HFSamplingPort", "HFQueuingPort", "CANPort")
        
        print("HFNAMELIST", hfnamelist)

        for functype in functypes:
            print("FUNCTIONTYPE:", functype)
            for xha in self.xroot.e.get(functype, []):
                if xha.a.Name in hfnamelist:                   
                    for porttype in porttypes:
                        msgtype = self.porttype2msgtype[porttype]
                        for xport in xha.e.get(porttype, []):
                            dataflowreflist = xport.e.get("Dataflow_Ref", [])
                            if len(dataflowreflist) > 1:
                                logger.nerror("More than one Dataflow_ref [%d]" % len(dataflowreflist),
                                      HF=xha.a.Name, PORT=xport.a.Name, DF=dataflowreflist[0].a.SrcName
                                )
                            for xrp in xport.e.get('RP', []):
                                self.processOneRP(xha, msgtype, xport, dataflowreflist, xrp, hfnamelist)

    # ----------------------------------------------------------------------
    def processOneRP(self, xha, msgtype, xport, dataflowreflist, xrp, hfnamelist):
        '''
        Process one RP:
        Locate corresponding DP either by the Pub_Ref or the GW_Pub_Ref back reference
        Do all checks and create a bunch of information for the signal and for the message
        '''
        # local helper
        def alreadySubscribedInPort(xport, xsig, isgw):
            '''
            check of xsig is subscribed by a pubref in the current port
            if xsig is in a gateway, we have to check if a GW_Puh_Ref is pointing to
            an RP in the current port
            Else we have to check if the  ...
            
            '''
            if isgw:
                for xgwpref in xsig.e.get("Gw_Pub_Ref", []):
                    tgt = self.xindex[xgwpref.a.DestGuid]
                    if tgt.isChildOf(xport):
                        return True
                return False
            else:
                for r in xport.e.get("RP", []):
                    for pr in r.e.get("Pub_Ref", []):
                        if pr.a.SrcGuid == xsig.a.Guid:
                            return True
                return False

        def expandA429LabelSubscribe(rprec, xport, isgw):
            '''
            Expand an RP subscribing a A429 Label Word (instead of the individual signals)
            Create an RP with correspond info for each signal of the label (including label SDI, etc)
            The RP is linked to the corresponding signal and will create one line in the excel ICD
            If RPs linked to signals of the label already exist, they are not duplicated.
            '''
            for xsig in rprec.dp.e.get('DP', []):
                if not alreadySubscribedInPort(xport, xsig, isgw):
                    # create new rp object by copyin current RP:
                    if isgw:
                        xsigclass = xsig
                    else:
                        xsigclass = self.getClass(xsig)
                    newrp = Bunch(
                        skip    = '',
                        rpName  = rprec.rpName + '.' + xsig.a.Name,
                        PubrefName = rprec.PubrefName  + '.' + xsig.a.Name,
                        msg     = rprec.msg,
                        dfref   = rprec.dfref,
                        dp      = xsig,
                        dpclass = xsigclass,
                    )
                    rpkey = (xha.a.Name, newrp.rpName)
                    addRp(newrp, rpkey, skip=False)
                    
        def isRpInList(rprec):
            for rp in self.rplist[rprec.rpName]:
                if rp.PubrefName == rprec.PubrefName \
                    and rp.dp == rprec.dp \
                    and rp.msg == rprec.msg:
                    return True

            return False
        
        def addRp(rprec, rpkey, skip=False):
            if skip:
                rprec.skip = '#'
            else:
                rprec.skip = ''

            self.rpuniq[rpkey] = rprec
                
            rpname = rpkey[1] 
            if not rpname in self.rplist:
                self.rplist[rpname] = [rprec]
            elif not isRpInList(rprec):
                self.rplist[rpname].append(rprec)

        def isDuplicateRp(rpkey):
            if rpkey in self.rpuniq:
                logger.nerror("Duplicate RP", 
                    HF=xha.a.Name, PORT=xport.a.Name, RP=xrp.a.Name,
                )
                return True
            else:
                return False

        # ------------------------------------------------------
        # start of Function Body
        # ------------------------------------------------------

        # gather the results in a Bunch
        rprec = Bunch(
                skip            = '',
                rpName          = xrp.a.Name, 
                dfref           = None,
                dp              = None,
                dpclass         = None,
                msg             = None,
                PubrefName      = None)
        rpkey = (xha.a.Name, xrp.a.Name)

        # check for duplicate RP Name. This is not allowed and we discard this RP
        if isDuplicateRp(rpkey):
            return  # nothing else we can do

        # check for pubref
        pubreflst = xrp.e.get("Pub_Ref", [])
        if not pubreflst: 
            logger.nerror("RP without Pub_Ref",
                  HF=xha.a.Name, PORT=xport.a.Name, RP=xrp.a.Name
            )
            addRp(rprec, rpkey, skip=True)
            return # nothing else we can do. RP will be in the signal table but only with its name

        # multiple pubrefs are always an error, but we try our best and use the first in the list
        # for further processing
        if len(pubreflst) > 1:
            logger.nerror("Multiple Pub_Refs for one RP", 
                  HF=xha.a.Name, PORT=xport.a.Name, RP=xrp.a.Name
            )
        pubref = pubreflst[0]
        rprec.PubrefName = pubref.a.SrcName
        
        # either the RP is referenced by Gateway or the TX Signal is the Pubref 
        xdp = self.gwsignalxref.get(xrp.a.Guid)
        if xdp:
            isgw = True
        else:
            xdp = self.xindex.get(pubref.a.SrcGuid, None)
            isgw = False
        
        if not xdp: 
            logger.nerror("No DP message found for RP", 
                  HF=xha.a.Name, PORT=xport.a.Name, RP=xrp.a.Name)
            addRp(rprec, rpkey, skip=True)
            return  # nothing else we can do
        
        # now get the message containing the DP
        xmsg = _getParentMsg(xdp, msgtype)
        if not xmsg:
            # xmsg is bit an AFDX DP, so there is a mess with Gateways and Pubrefs.
            logger.nerror("Pubref/Gateway mismatch: sender is not on same bus type",
                          HF=xha.a.Name, PORT=xport.a.Name, RP=xrp.a.Name
            )
            addRp(rprec, rpkey, skip=True)
            return # nothing else we can do on this RP

        # Check if data source is one of the systems we are stimulating.
        # In this case, we skip the signal, since we don't need to stimulate this.
        # When we process the RP we will generate a receiver for it for monitoring
        
        txlru = _getTopNode(xmsg)
        if txlru.a.Name in hfnamelist:
            # no need to process this further. We also don't store it, it is simply discarded.
            return 
            
        if isgw:
            xdpclass  = xdp
            xmsgclass = xmsg
        else:
            xdpclass  = self.getClass(xdp)
            xmsgclass = self.getClass(xmsg)

        # link to message object
        if xmsg.a.Guid in self.rxMessagelist:
            msgrec = self.rxMessagelist[xmsg.a.Guid]
            if len(hfnamelist) > 0: #mode: merged
                portDefined = False
                for port in msgrec.rxport:
                    if port.a.Name in xport.a.Name:
                        portDefined = True
                        break
                if not portDefined:
                    msgrec.rxport.append(xport)  
        else:
            msgrec = Bunch(msgtype=msgtype, txmsg=xmsg, txmsgclass=xmsgclass, rxport=[xport])
            self.rxMessagelist[xmsg.a.Guid] = msgrec
        
        rprec.dp      = xdp
        rprec.dpclass = xdpclass
        rprec.msg     = msgrec
    
        # check consistency of Dataflow_Ref with Pub_Ref
        if dataflowreflist:
            ok = False
            for dfref in dataflowreflist:
                if self.checkContainment(xdp, self.xindex[dfref.a.SrcGuid]):
                    rprec.dfref = dfref
                    ok = True
                    break

            if not ok:
                logger.nerror("Bad Dataflow_ref containment", 
                      HF=xha.a.Name, PORT=xport.a.Name, RP=xrp.a.Name,
                      DP=xdp.a.Guid,
                      DF=dataflowreflist[0].a.SrcGuid
                )
                
        # if the RP is linked to a A429 Label (instead of its signals)
        # expand the RP so each signal is linked individually
        # If the expanded signal does not already exists in the same port, add it
        
        if rprec.dp.tag == "A429Word":
            expandA429LabelSubscribe(rprec, xport, isgw)
        else:
            addRp(rprec, rpkey, skip=False)
       
                       

    # ----------------------------------------------------------------------
    def gatherRxSignalDetails(self):

        def getDSAttrib(rp, xdp, xds, xdpclass, xdsclass):
            rp.DsName        = xds.a.Name
            rp.ByteOffsetFSB = _getAttrib(xdsclass, "ByteOffsetFSF", int)
            rp.ByteOffsetDS  = _getAttrib(xdsclass, "ByteOffsetWithinMsg", int)
            rp.ByteSizeDS    = _getAttrib(xdsclass, "DataSetSize", int)

        def getDPDSAttrib(rp, xdp, xds, xdpclass, xdsclass):
            rp.SigName       = xdp.a.Name
            rp.DsName        = xds.a.Name
            rp.ByteOffsetFSB = _getAttrib(xdsclass, "ByteOffsetFSF", int)
            rp.ByteOffsetDS  = _getAttrib(xdsclass, "ByteOffsetWithinMsg", int)
            rp.ByteSizeDS    = _getAttrib(xdsclass, "DataSetSize", int)
            rp.BitOffset     = _getAttrib(xdpclass, "BitOffsetWithinDS", int)
            rp.BitSize       = _getAttrib(xdpclass, "ParameterSize", int)
            rp.Encoding      = _getAttrib(xdpclass, "DataFormatType")
            if rp.Encoding == "BNR" or rp.Encoding == "BCD":
                rp.LsbValue        = _getAttrib(xdpclass, "LsbRes", float, default=1)
            else:
                rp.LsbValue        = 1

        def getDPDSAttribA429(rp, xdp, xds, xdpclass, xdsclass):
            rp.SigName       = xdp.a.Name
            rp.DsName        = xds.a.Name
            rp.ByteOffsetFSB = _getAttrib(xdsclass, "ByteOffsetFSF", int)
            rp.ByteOffsetDS  = _getAttrib(xdsclass, "ByteOffsetWithinMsg", int)
            rp.ByteSizeDS    = _getAttrib(xdsclass, "DataSetSize", int)
            
            rp.BitOffset     = _getAttrib(xdpclass, "BitOffsetWithinDS", int)

            rp.BitSize       = _getAttrib(xdpclass, "ParameterSize", int)
            rp.Encoding      = _getAttrib(xdpclass, "DataFormatType")
            if rp.Encoding == "BNR":
                rp.LsbValue        = _getAttrib(xdpclass, "LsbRes", float)
            else:
                rp.LsbValue        = 1

            # The ICD contains many errors regarding BitOffset of Signals embedded in 429 Words
            # We do a plausibility check and repair the value if it is wrong
            # get parent (A429Word) offset and check wether signal offset is within the word
            # If not compute the most plausible value but create an entry in the log
            a429wordoffset = _getAttrib(xdpclass.parent, "BitOffsetWithinDS", int)
            if rp.BitOffset < 0 or rp.BitOffset > 32:
                logger.nerror("BitOffset of embedded A429 Word inconsistent", DP=xdp.a.Name, DS=xds.a.Name)

            if a429wordoffset is not None:
                rp.BitOffset = rp.BitOffset % 32 + a429wordoffset

        def getCANDPAttrib(rp, xdp, xdpclass):
            rp.SigName       = xdp.a.Name
            rp.DsName        = "N/A"
            rp.ByteOffsetFSB = 0
            rp.ByteOffsetDS  = 0
            rp.ByteSizeDS    = _getAttrib(xdpclass.parent, "MessageSize", int)
            rp.BitOffset     = _getAttrib(xdpclass, "BitOffsetWithinDS", int)
            rp.BitSize       = _getAttrib(xdpclass, "ParameterSize", int)
            rp.Encoding      = _getAttrib(xdpclass, "DataFormatType")
            
        def consistencyCheck(rp):
            if (rp.ByteOffsetDS + rp.ByteSizeDS) > rp.msg.Length:
                rp.skip = '#'
                rp.msg.skip = '#'
                logger.nerror("RP Dataset size inconsistent with message size, skipped.", 
                              DS=rp.DsName, DSsize=rp.ByteSizeDS, 
                              Msg=rp.msg.Message, MsgSize=rp.msg.Length)
            
        #------ start function body -------------------------
        
        for rpreclist in self.rplist.values():
            for rprec in rpreclist:
                # initialize all attributes to none
                rprec.LruName         = ''
                rprec.MsgName         = ''
                rprec.nesting         = ''
                rprec.DsName          = ''
                rprec.SigName         = ''
                rprec.SourceSelection = ''
                rprec.ByteOffsetFSB   = ''
                rprec.ByteOffsetDS    = ''
                rprec.ByteSizeDS      = ''
                rprec.BitOffset       = ''
                rprec.BitSize         = ''
                rprec.LsbValue        = ''
                rprec.Encoding        = ''
                
                if not rprec.dp:
                    # no further processing is possible
                    continue

                rprec.LruName         = rprec.msg.Lru
                rprec.MsgName         = rprec.msg.Message
                rprec.nesting         = _getDSPath(rprec.dp, rprec.msg.msgtype)

                xdp           = rprec.dp
                xdpclass      = rprec.dpclass
                path          = rprec.nesting 


                if path == 'A664Message.DS.DP':
                    # for gateways, this is the object itself
                    getDPDSAttrib(rprec, xdp, xdp.parent, xdpclass, xdpclass.parent)
                    if rprec.ByteOffsetFSB == 0 and rprec.ByteOffsetDS == 0:
                        # we find this for A661 Blocks
                        rprec.ByteOffsetFSB = None
                    
                    if rprec.ByteOffsetFSB is not None:
                        rprec.SourceSelection = 'FRESH,FSB'
                    else:
                        rprec.SourceSelection = 'FRESH'
    
                elif path == 'A664Message.DS.A429Word.DP':
                    
                    getDPDSAttribA429(rprec, xdp, xdp.parent.parent, xdpclass, xdpclass.parent.parent)
                    rprec.SourceSelection = 'FRESH,FSB'
                    # lookup SSM in sibling DPs
                    ssmtype = _getSSMType(xdpclass)
                    if ssmtype:
                        rprec.SourceSelection += ',' + ssmtype
                elif path == 'A664Message.DS.A429Word':
                    # Already expanded in ProcessRP
                    logger.nerror("Unsupported signal nesting [%s]" % path, RP=rprec.rpName)
                elif path == 'A664Message.DS.CANMessage.DP':
                    getDPDSAttrib(rprec, xdp, xdp.parent.parent, xdpclass, xdpclass.parent.parent)
                    rprec.SourceSelection = 'FRESH, FSB'
                elif path == 'A664Message.DS.CANMessage.A429Word.DP':
                    getDPDSAttrib(rprec, xdp, xdp.parent.parent.parent, xdpclass, xdpclass.parent.parent.parent)
                    rprec.SourceSelection = 'FRESH,FSB'
                    # lookup SSM in sibling DPs
                    ssmtype = _getSSMType(xdpclass)
                    if ssmtype:
                        rprec.SourceSelection += ',' + ssmtype
                elif path == 'A664Message.DS.CANMessage':
                    logger.nerror("Unsupported signal nesting [%s]" % path, RP=rprec.rpName)
                elif path == 'A664Message.DS.CANMessage.A429Word':
                    logger.nerror("Unsupported signal nesting [%s]" % path, RP=rprec.rpName)
                elif path == 'CANMessage.DP':
                    getCANDPAttrib(rprec, xdp, xdpclass)
                else:
                    logger.nerror("Unsupported signal nesting [%s]" % path, RP=rprec.rpName)
                    
                consistencyCheck(rprec)
    
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    def consistencyCheckDPs(self):
        for dp in self.dplist.values():
            if (dp.ByteOffsetDS + dp.ByteSizeDS) > dp.msg.Length:
                dp.skip = '#'
                dp.msg.skip = '#'
                logger.nerror("DP Dataset size inconsistent with message size, skipped.", 
                              DS=dp.DsName, DSsize=dp.ByteSizeDS, 
                              Msg=dp.msg.Message, MsgSize=dp.msg.Length)

    def processFunctionDPs(self, hfnamelist):
        '''
        Traverse hosted function/application and create a list of DPs with associated information
        
        '''
        def processDP(hfname, xdp, xpath, xds, xmsg, msgtype ): 
            '''
            process one DP, either directly below DS or inside a A429Word or CAN Message
            '''
            # gather the results in a Bunch
            xdpclass  = self.xindex[xdp.a.GuidDef]
            xmsgclass = self.xindex[xmsg.a.GuidDef]
            xdsclass  = self.xindex[xds.a.GuidDef]

            # link to message object
            if xmsg.a.Guid in self.txMessagelist:
                msgrec = self.txMessagelist[xmsg.a.Guid]
            else:
                msgrec = Bunch(msgtype=msgtype, txmsg=xmsg, txmsgclass=xmsgclass, rxport=None)
                self.txMessagelist[xmsg.a.Guid] = msgrec
                            
            signame = xdp.a.Name
            for o in xpath:
                signame = o.a.Name + '.' + signame
            sigkey = (hfname, xmsg.a.Name, xds.a.Name, signame)

            dprec = Bunch(
                dpName          = signame, 
                dpclass         = self.xindex[xdp.a.GuidDef],
                msg             = msgrec,
                LruName         = hfname,
                DsName          = xds.a.Name,
                MsgName         = xmsg.a.Name,
                Validity        = "",
                ByteOffsetFSB   = None,
                ByteOffsetDS    = _getAttrib(xdsclass, "ByteOffsetWithinMsg", int),
                ByteSizeDS      = _getAttrib(xdsclass, "DataSetSize", int),
                BitOffset       = _getAttrib(xdpclass, "BitOffsetWithinDS", int),
                BitSize         = _getAttrib(xdpclass, "ParameterSize", int),
                Encoding        = _getAttrib(xdpclass, "DataFormatType"),
                LsbValue        = 1,
                Consumer        = ""
            )

            if xdsclass.a.DsDataProtocolType != 'A664_FSS':
                dprec.ByteOffsetFSB = _getAttrib(xdsclass, "ByteOffsetFSF", int, default=0)
                if dprec.ByteOffsetFSB == 0 and dprec.ByteOffsetDS == 0:
                    dprec.Validity = ''
                else:
                    if xpath and xpath[0].tag == "A429Word":
                        dprec.Validity = 'FSB, ' + _getSSMType(self.xindex[xpath[0].a.GuidDef])
                    else:
                        dprec.Validity = "FSB"

            if dprec.Encoding == "BNR":
                dprec.LsbValue        = _getAttrib(xdpclass, "LsbRes", float)

            if sigkey in self.dplist:
                logger.nerror("Duplicate DP name [%s]" % str(sigkey))
            else:
                self.dplist[sigkey] = dprec
            
            consumerlist = self.pubrefxref[xdp.a.Guid]
            consumerlist += self.pubrefxref[xdp.parent.a.Guid] # also add those referencing the parent 
                                                               # (i.e. the inclosing A429Word)
            sep = ''
            for consumer in consumerlist:
                dprec.Consumer += sep + consumer[0].a.Name
                sep = ','
                
        
        #------- start of function -------------------------------
        functypes = ("HostedFunction", "A653ApplicationComponent")
        porttypes = ("HFSamplingPort", "HFQueuingPort", "A653SamplingPort", "A653QueuingPort")
        
        for functype in functypes:
            for xha in self.xroot.e.get(functype, []):
                if xha.a.Name in hfnamelist:
                    hfname = xha.a.Name
                    for porttype in porttypes:
                        for xport in xha.e.get(porttype, []):
                            for xmsg in xport.e.get('A664Message', []):
                                for xds in xmsg.e.get('DS', []):
                                    for xdp in xds.e.get('DP', []):
                                        processDP(hfname, xdp, (), xds, xmsg, "A664Message")
                                    for xa4 in xds.e.get('A429Word', []):
                                        for xdp in xa4.e.get('DP', []):
                                            processDP(hfname, xdp, (xa4, ), xds, xmsg, "A664Message")
                                    for xcanmsg in xds.e.get('CANMessage', []):
                                        for xdp in xcanmsg.e.get('DP', []):
                                            processDP(hfname, xdp, (xcanmsg, ), xds, xmsg, "A664Message")
                                        for xa4 in xcanmsg.e.get('A429Word', []):
                                            for xdp in xa4.e.get('DP', []):
                                                processDP(hfname, xdp, (xa4, xcanmsg), xds, xmsg, "A664Message")
                                
                       
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------               

    def gatherRxMessageDetails(self):
        for msg in self.rxMessagelist.values():
            if msg.msgtype == "A664Message":
                self.gatherOneAfdxRxMessageDetails(msg)
            elif msg.msgtype == "CANMessage":
                self.gatherOneCanRxMessageDetails(msg)


    def gatherOneAfdxRxMessageDetails(self, msg):
        '''
        Fill the details needed by the XLS table
        - Lru             HF/HA name used (together with msg name) as key to match from the signal tab. 
        - Message         Message name used (together with lru name) as key to match from the signal tab. 
        - Rate            Transmit / Receive rate: used to determine freshness and for test bench configuration
        - Port ID         Port ID of receiving port, used to configure the APEX ports
        - Vlid            Test system configuration only
        - SubVl           Test system configuration only
        - BAG             Test system configuration only
        - MTU             Test system configuration only
        - Source MAC      Test system configuration only
        - Source IP       Test system configuration only
        - Source UDP      Test system configuration only
        - EdeEnabled      Test system configuration only
        - Source EDE ID   Test system configuration only
        - Destination IP  Test system configuration only
        - Destination UDP Test system configuration only
        - Length          Test system configuration only
        - QueueLength     Used for APEX port configuration system configuration only
        - Type:           Port Type or the receiving port (Queuing/Sampling)

        '''

        def getIpAddrType(vl, rxcomport):
            txport = vl.rx2txport[rxcomport.a.Name]
            return txport.a.IPDestAddrFormat

        def getMACAddress(lru):
            hw = self.hardwarexref.get(txlru.a.Hardware)
            if hw:
                physport = hw.get('A')
                if physport:
                    return physport.a.get("MACAddress", "")
            return ""
        

        txmsg      = msg.txmsg
        txmsgclass = msg.txmsgclass
        txport     = msg.txmsg.parent
        txportclass= txmsgclass.parent
        txlru      = _getTopNode(txport)
        rxport     = msg.rxport[0]
        rxportclass= self.getClass(rxport)
        
        rxlru      = _getTopNode(rxport)

        if rxport.tag.endswith("SamplingPort"):
            rxtype = "SAMPLING"
        else:
            rxtype = "QUEUEING"
        
        if rxport.tag.endswith("QueuingPort"):
            msg.QueueLength = _getAttrib(rxportclass, "QueueLength", int, default=1)
        else:
            msg.QueueLength = 1

        msg.Lru       = txlru.a.Name
        msg.Message   = txmsg.a.Name
        msg.Length    = _getAttrib(txmsgclass, "MessageSize", int)
        msg.Overhead  = _getAttrib(txmsgclass, "MessageOverhead", int)
        msg.RxLength  = _getAttrib(rxportclass, "MessageSize", int)
        msg.Rate      = _getAttrib(txportclass,  "RefreshPeriod", float)
        msg.RxRate    = _getAttrib(rxportclass,  "SamplePeriod", float)
        msg.Type      = rxtype
        msg.Vlid      = _getAttrib(txmsg, 'VLID', int)
        msg.SubVl     = _getAttrib(txmsg, 'SubVLID', int)

        msg.PortID    = None
        msg.PortName  = None
        msg.BAG       = None
        msg.MTU       = None
        msg.SourceMAC = None
        msg.SourceIP  = None
        msg.SourceUDP = None
        msg.DestIP    = None
        msg.DestUDP   = None
        if msg.Vlid:
            vl = self.vlxref.get(msg.Vlid)
            if vl:
                rxcomport       = vl.rxports.get(rxlru.a.Name + '.' + rxport.a.Name)
                if not rxcomport:
                    logger.nerror("No RX COM Port found", HF=rxlru.a.Name, PORT=rxport.a.Name)
                else:
                    msg.PortID      = _getAttrib(rxcomport, "ID", int)
                    if len(msg.rxport) > 1: # makes no sense in merged mode
                        msg.PortID = 0
                    portNames = []
                    #msg.PortName    = rxport.a.Name
                    for port in msg.rxport:
                        lru = _getTopNode(port)
                        if len(msg.rxport) > 1:
                            portNames.append(lru.a.Name + "." + port.a.Name)
                        else:
                            portNames.append(port.a.Name)
                    msg.PortName = ",".join(portNames)
                    msg.DestUDP     = _getAttrib(rxcomport, "UdpDstId", int)

                txcomport       = vl.txports.get(txlru.a.Name + '.' + txport.a.Name)
                if not txcomport:
                    logger.nerror("No TX COM Port found", HF=txlru.a.Name, PORT=txport.a.Name)
                else:
                    msg.SourceUDP   = _getAttrib(txcomport, "UdpSrcId", int)
                    msg.EdeSourceID = _getAttrib(txcomport, "ID", int)

                msg.SourceMAC   = getMACAddress(txlru)
                
                msg.SourceIP    = _getAttrib(txlru, 'IpAddress', default='10.0.0.1')
                if txcomport.a.IPDestAddrFormat == "UNICAST":
                    msg.DestIP      = _getAttrib(rxlru, 'IpAddress')
                else:
                    msg.DestIP      = _makeMulticastIpAddr(msg.Vlid)
                msg.BAG         = _getAttrib(vl.xvl, "BAG", float)
                msg.MTU         = _getAttrib(vl.xvl, "MTU", int)
                msg.EdeEnabled  = _getAttrib(vl.xvl, 'EdeEnable', bool)
            else:
                logger.nerror("VL not found", VLID=msg.Vlid, MSG=txmsg.a.Name)

    def gatherOneCanRxMessageDetails(self, msg):
        '''
        Fill the details needed by the XLS table
        - Lru             HF/HA name used (together with msg name) as key to match from the signal tab. 
        - Message         Message name used (together with lru name) as key to match from the signal tab. 
        - Rate            Transmit / Receive rate: used to determine freshness and for test bench configuration
        - Length          Test system configuration only
        - CanMsgID        CanID of message
        - PhysPort        Physical port the message is received on
        '''

        txmsg      = msg.txmsg
        txmsgclass = msg.txmsgclass
        txport     = msg.txmsg.parent
        txportclass= txmsgclass.parent
        txlru      = _getTopNode(txport)
        rxport     = msg.rxport[0]
        rxlru      = _getTopNode(rxport)

        msg.Lru         = txlru.a.Name
        msg.Message     = txmsg.a.Name
        msg.Length      = _getAttrib(txmsgclass, "MessageSize", int)
        msg.Rate        = _getAttrib(txportclass,  "RefreshPeriod", float)
        
        txid = _getAttrib(txport, "MessageID")
        rxid = _getAttrib(rxport, "MessageID")
        if txid != rxid:
            logger.nerror("CAN Message ID mismatch between TX and RX", TXPORT=txport.a.Name, RXPORT=rxport.a.Name)
       
        msg.CanMsgID  = _getAttrib(rxport, "MessageID")
        msg.PhysPort  = _getAttrib(rxport, "Physical")

    # ----------------------------------------------------------------------               

    def gatherTxMessageDetails(self):
        '''
        Fill the details needed by the XLS table
        - Lru             HF/HA name used (together with msg name) as key to match from the signal tab. 
        - Message         Message name used (together with lru name) as key to match from the signal tab. 
        - Rate            Transmit / Receive rate: used to determine freshness and for test bench configuration
        - Port ID         Port ID of receiving port, used to configure the APEX ports
        - Vlid            Test system configuration only
        - SubVl           Test system configuration only
        - BAG             Test system configuration only
        - MTU             Test system configuration only
        - Source MAC      Test system configuration only
        - Source IP       Test system configuration only
        - Source UDP      Test system configuration only
        - EdeEnabled      Test system configuration only
        - Source EDE ID   Test system configuration only
        - Destination IP  Test system configuration only
        - Destination UDP Test system configuration only
        - Length          Test system configuration only
        - QueueLength     Used for APEX port configuration system configuration only
        - Type:           Port Type or the receiving port (Queuing/Sampling)

        '''


        def getMACAddress(lru):
            '''
            Find the mac Address of an LRU
            '''
            hw = self.hardwarexref.get(txlru.a.Hardware)
            if hw:
                physport = hw.get('A')
                if physport:
                    return physport.a.get("MACAddress", "")
            return ""

        def findDestinationUDP(vl, txcomport):
            '''
            Find the destination UDP Address for a transmit port
            '''
            rxports = vl.tx2rxports[txcomport.a.Name]
            udps = [p.a.UdpDstId for p in rxports]
            udps = set(udps)
            if len(udps) == 1:
                return int(list(udps)[0])
            elif len(udps) > 1:
                logger.nerror("Destination UDP not unique", VLID=msg.Vlid, MSG=txmsg.a.Name)
                return None
            else:
                logger.nerror("No Destination UDP address found", VLID=msg.Vlid, MSG=txmsg.a.Name)
                return None


        def findUnicastIpAddr(vl, txcomport):
            '''
            Find the unicast IP Address for a transmit port
            '''
            rxports = vl.tx2rxports[txcomport.a.Name]
            ipaddrset = set()

            # traverse receive ports receiving from the tx port
            for rxp in rxports:
                # traverse application ports linked to the receive com port
                for pref in rxp.e.Port_Ref:
                    # get corresponding application (HF or HA) from the Xref build during initialization
                    # extract the IP address and add it to our result set.
                    x = self.appportXref.get(pref.a.Name)
                    if x:
                        hf, port = x
                        ipaddr = hf.a.get("IpAddress")
                        ipaddrset.add(ipaddr)
                    else:
                        logger.nerror("No Destination IP address found", VLID=msg.Vlid, MSG=txmsg.a.Name)

            # Since we are looking for a UNICAST address, we should find exactly one
            if len(ipaddrset) == 1:
                return list(ipaddrset)[0]
            elif len(ipaddrset) > 1:
                logger.nerror("Destination IP Address not unique", VLID=msg.Vlid, MSG=txmsg.a.Name)
                return None
            else:
                logger.nerror("No Destination IP Address found", VLID=msg.Vlid, MSG=txmsg.a.Name)
                return None
        
        # -------------------------------------------------------------------------------------------
        # Start of function
        # -------------------------------------------------------------------------------------------
        for msg in self.txMessagelist.values():
            txmsg      = msg.txmsg
            txmsgclass = msg.txmsgclass
            txport     = msg.txmsg.parent
            txportclass= txmsgclass.parent
            txlru      = _getTopNode(txport)

            if txport.tag.endswith("SamplingPort"):
                txtype = "SAMPLING"
                msg.QueueLength = 1
            else:
                txtype = "QUEUEING"
                msg.QueueLength = _getAttrib(txportclass, "QueueLength", int, default=1)

            msg.Lru       = txlru.a.Name
            msg.Message   = txmsg.a.Name
            msg.Length    = _getAttrib(txmsgclass, "MessageSize", int)
            msg.Overhead  = _getAttrib(txmsgclass, "MessageOverhead")
            msg.RxLength  = None
            msg.Rate      = _getAttrib(txportclass,  "RefreshPeriod", float)
            msg.RxRate    = None
            msg.Type      = txtype
            msg.Vlid      = _getAttrib(txmsg, 'VLID', int)
            msg.SubVl     = _getAttrib(txmsg, 'SubVLID', int)

            msg.PortID    = None
            msg.PortName  = None
            msg.BAG       = None
            msg.MTU       = None
            msg.SourceMAC = None
            msg.SourceIP  = None
            msg.SourceUDP = None
            msg.DestIP    = None
            msg.DestUDP   = None
            if msg.Vlid:
                vl = self.vlxref.get(msg.Vlid)
                if vl:
                    txcomport       = vl.txports.get(txlru.a.Name + '.' + txport.a.Name)
                    if not txcomport:
                        logger.nerror("No TX COM Port found", HF=txlru.a.Name, PORT=txport.a.Name)
                    else:
                        msg.PortID      = _getAttrib(txcomport, "ID", int)
                        msg.PortName    = txport.a.Name
                        msg.SourceUDP   = _getAttrib(txcomport, "UdpSrcId", int)
                        msg.EdeSourceID = _getAttrib(txcomport, "ID", int)
                        
                        # find destination UDP
                        msg.DestUDP = findDestinationUDP(vl, txcomport)

                        # find destination IP
                        if txcomport.a.IPDestAddrFormat == 'MULTICAST':
                            msg.DestIP = _makeMulticastIpAddr(msg.Vlid)
                        else:
                            msg.DestIP = findUnicastIpAddr(vl, txcomport)
                            
    
                    msg.SourceMAC   = getMACAddress(txlru)
                    msg.SourceIP    = _getAttrib(txlru, 'IpAddress', default='10.0.0.1')
                    msg.BAG         = _getAttrib(vl.xvl, "BAG", float)
                    msg.MTU         = _getAttrib(vl.xvl, "MTU", float)
                    msg.EdeEnabled  = _getAttrib(vl.xvl, 'EdeEnable', bool)
                else:
                    logger.nerror("VL not found", VLID=msg.Vlid, MSG=txmsg.a.Name)
            
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    def makeVLxref(self):
        vls = self.xroot.e.VirtualLinks[0]
        for xvl in vls.e.VirtualLink:
            rxports     = dict()
            txports     = dict()
            tx2rxports   = defaultdict(list)

            try:
                vlid = int(xvl.a.get("ID"))
            except:
                logger.nerror("VL without ID", VLNAME=xvl.a.Name)
                continue
            
            for xrp in xvl.e.get("ComPortRx", []):
                for pref in xrp.e.Port_Ref:
                    key = pref.a.Name
                    rxports[key] = xrp
                for txref in xrp.e.TxPort_Ref:
                    key = txref.a.Name.split('.', 1)[1]
                    tx2rxports[key].append(xrp)

            for xtp in xvl.e.get("ComPortTx", []):
                for pref in xtp.e.Port_Ref:
                    key = pref.a.Name
                    txports[key] = xtp

            self.vlxref[vlid] = Bunch(xvl = xvl, rxports=rxports, txports=txports, tx2rxports=tx2rxports)
    
    # ----------------------------------------------------------------------
    def makeHardwareXref(self):
        '''
        Create index for Hardware: 
            lookup hardware by name with port dictionary indexed by port name
        '''
        def makePortDict(xlru):
            portdict = {}
            for porttype, portlist in xlru.e.items():
                if porttype.endswith("PhysPort"):
                    for port in portlist:
                        portdict[port.a.Name] = port
            return portdict
        
        self.hardwarexref = dict()
        for xlru in self.xroot.e.LRU + self.xroot.e.RIU:
            self.hardwarexref[xlru.a.Name] = makePortDict(xlru)
            
        for xccr in self.xroot.e.CCR:
            for xmod in xccr.e.GPM:
                self.hardwarexref[xccr.a.Name + '.' + xmod.a.Name] = makePortDict(xmod)

    # ----------------------------------------------------------------------
    def makeRpXref(self):
        '''
        Traverse hosted function/application and create an index RP->DP
        '''
        functypes = ("HostedFunction", "A653ApplicationComponent")
        porttypes = ("HFSamplingPort", "HFQueuingPort", "A653SamplingPort", "A653QueuingPort", "CANPort")
        
        for functype in functypes:
            for xha in self.xroot.e.get(functype, []):
                for porttype in porttypes:
                    for xport in xha.e.get(porttype, []):
                        for xrp in xport.e.get('RP', []):
                            for pubref in xrp.e.get("Pub_Ref", []):
                                self.pubrefxref[pubref.a.SrcGuid].append((xha, xport, xrp))
                                
        
    # ----------------------------------------------------------------------
    def makePortXref(self):
        '''
        Traverse hosted function/application and create an index Port Name -> Port
        '''
        functypes = ("HostedFunction", "A653ApplicationComponent")
        porttypes = ("HFSamplingPort", "HFQueuingPort", "A653SamplingPort", "A653QueuingPort")
        
        for functype in functypes:
            for xha in self.xroot.e.get(functype, []):
                for porttype in porttypes:
                    for xport in xha.e.get(porttype, []):
                        self.appportXref[xha.a.Name + '.' + xport.a.Name] = (xha, xport)


    # ----------------------------------------------------------------------
    # Format the output to Excel
    # ----------------------------------------------------------------------
    
    inSigColumns = (
        # header,         value,                len
          ("Skip",        "skip",                5),
          ("RpName",      "rpName",             40),
          ("Pubref",      "PubrefName",         40),
          ("Lru",         "LruName",            30),
          ("Message",     "MsgName",            40),
          ("DataSet",     "DsName",             40),
          ("Signal",      "SigName",            40),
          ("SSEL",        "SourceSelection",    15),
          ("FsbOffset",   "ByteOffsetFSB",      10),
          ("DSOffset",    "ByteOffsetDS",       10),
          ("DSSize",      "ByteSizeDS",         10),
          ("SigType",     "Encoding",           10),
          ("SigOffset",   "BitOffset",          10),
          ("SigSize",     "BitSize",            10),
          ("LsbValue",    "LsbValue",           10),
          ("Comment",     None,                 40),
    )
    
    outSigColumns = (
        # header,         value,                len
          ("Skip",        "skip",                5),
          ("DpName",      "dpName",             40),
          ("Lru",         "LruName",            30),
          ("DataSet",     "DsName",             40),
          ("Message",     "MsgName",            40),
          ("Validity",    "Validity",           15),
          ("FsbOffset",   "ByteOffsetFSB",      10),
          ("DSOffset",    "ByteOffsetDS",       10),
          ("DSSize",      "ByteSizeDS",         10),
          ("SigType",     "Encoding",           10),
          ("SigOffset",   "BitOffset",          10),
          ("SigSize",     "BitSize",            10),
          ("LsbValue",    "LsbValue",           10),
          ("Consumer",    "Consumer",           30),
          ("Comment",     None,                 40),
    )
   
    msgAfdxColumns = (
        # header,               value,           width
          ("Skip",              "skip",           5),
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
          ("EdeSourceId",       "EdeSourceID",   10),
          ("DestIP",            "DestIP",        15),
          ("DestUDP",           "DestUDP",       15),
          ("SourceMAC",         "SourceMAC",     15),
          ("SourceIP",          "SourceIP",      15),
          ("SourceUDP",         "SourceUDP",     10),
    )

    msgCanColumns = (
          ("Skip",              None,             5),
          ("Lru",               "Lru",           30),
          ("Message",           "Message",       40),
          ("Length",            "Length",        10),
          ("Rate",              "Rate",          10),
          ("CanMsgID",          "CanMsgID",      10),
          ("PhysPort",          "PhysPort",      20),
    )
    

    def formatOutput(self, outputfn):

        def msgfilter(msglist, msgtype):
            return [m for m in msglist if m.msgtype == msgtype]
        
        # build final Input Signal List.

        inSignals = []
        for rpreclist in self.rplist.values():
            inSignals += rpreclist

        inSignals.sort(key=lambda sig: (sig.LruName, sig.MsgName, sig.ByteOffsetDS, sig.BitOffset))
                           
        genExcelFile(outputfn, 
            (
                ("InputAfdxMessages", self.msgAfdxColumns, 
                    sorted(msgfilter(self.rxMessagelist.values(), "A664Message"), 
                           key=lambda msg: (msg.Lru, msg.Message)
                    )
                ),
                ("InputCanMessages", self.msgCanColumns, 
                    sorted(msgfilter(self.rxMessagelist.values(), "CANMessage"),
                           key=lambda msg: (msg.Lru, msg.Message)
                    )
                ),
                ("InputSignals",  self.inSigColumns, inSignals),
                ("OutputAfdxMessages", self.msgAfdxColumns, 
                    sorted(msgfilter(self.txMessagelist.values(), "A664Message"),
                           key=lambda msg: (msg.Lru, msg.Message)
                    )
                ),
                ("OutputCanMessages", self.msgCanColumns, 
                    sorted(msgfilter(self.txMessagelist.values(), "CANMessage"),
                           key=lambda msg: (msg.Lru, msg.Message)
                    )
                ),
                ("OutputSignals",  self.outSigColumns, 
                    sorted(self.dplist.values(), 
                           key=lambda sig: (sig.LruName, sig.MsgName, sig.ByteOffsetDS, sig.BitOffset)
                    )
                ),
            )
        )

    def processHostedFunctions(self, hfnamelist, outfilename):
        self.reset()

        logger.ninfo("Constructing RP Index")
        logger.progress("Constructing RP Index", 3)
        self.processFunctionRPs(hfnamelist)
    
        logger.ninfo("Attaching Message Details")
        logger.progress("Attaching Message Details", 3)
        self.gatherRxMessageDetails()
    
        logger.ninfo("Attaching Signal Details")
        logger.progress("Attaching Signal Details", 1)
        self.gatherRxSignalDetails()
    
        self.processFunctionDPs(hfnamelist)
        self.gatherTxMessageDetails()
        self.consistencyCheckDPs()
    
        logger.progress("Formatting Output", 2)
        if outfilename == None:
            outfilename = '-'.join(hfnamelist) + '-icd.xlsx'
        self.formatOutput(outfilename)       
        
# END OF CLASS


def processIcd(sourcedirs, hfnamelist, exclude=None, outfilename="", merge=True):

    xroot = icdReadAll(sourcedirs, exclude=exclude)
    worker = IcdProcessor(xroot)

    logger.ninfo("Constructing VL Cross Index")
    logger.progress("Constructing VL Cross Index", 1)
    worker.makeVLxref()

    logger.ninfo("Constructing Hardware Cross Index")
    logger.progress("Constructing Hardware Cross Index", 1)
    worker.makeHardwareXref()
    worker.makeRpXref()
    worker.makePortXref()

    logger.ninfo("Constructing Gateway Cross Index")
    logger.progress("Constructing Gateway Cross Index", 5)
    worker.makeGatewayReverseMap()

    if merge:
        print("processing", hfnamelist)
        worker.processHostedFunctions(hfnamelist, outfilename)
    else:
        for hf in hfnamelist:
            print("processing", hf)
            worker.processHostedFunctions([hf], outfilename)

    

def usage():
    print("iomGenXls [options] hostedfunctions -- icdpathlist")
    print("   options:")
    print("     --merge")
    print("     --workdir=work directory")
    print("     --loglevel=<TRACE|INFO|WARN|ERROR>")
    print("     --logfile=<filename>")
    print("     --exclude=<path>")
    print("     --output=<path>")
    print("     --help")
    print("   If --merge option is given, output file name option (--output or -o) is mandatory. Without merge, it will be ignored")



def main():
    # options + arguments
    opts, args = getopt.getopt(sys.argv[1:], 'hpmw:o:', ['output=', 'workdir=', 'loglevel=', 'logfile=', 'exclude=', 'merge', 'help', 'progress', 'console'])
    
    # get arguments
    if len(args) < 2:
        usage()
        sys.exit(1)
    
    # A -- separates the hfname list from the source dir list.

    hfnamelist = []
    sourcedirs = []
    part = 1
    for x in args:
        if x == "--":
            part = 2
        elif part == 1:
            hfnamelist.append(x)
        elif part == 2:
            sourcedirs.append(x) 
    
    if part == 1:
        # no --, so to be compatible first argument is HF, rest are directories
        sourcedirs = hfnamelist[1:]
        hfnamelist = hfnamelist[:1]
            
    loglevel = logger.ERROR
    exclude  = '*/Default Configurations*'
    workdir  = '.'
    logprogress = False
    logconsole  = True
    merge       = False
    outfn       = None
    logfile     = None

    loglevels = {
        'INFO'  : logger.INFO,
        'WARN'  : logger.WARN,
        'ERROR' : logger.ERROR,
        'TRACE' : logger.TRACE,
    }

    # parse options
    for o, a in opts:
        if o in ['-h', '--help']:
            usage()
            return -1
        if o in ('-m', '--merge'):
            merge = True
        elif o in [ '--output', '-o']:
            outfn = a
        elif o in [ '--loglevel']:
            loglevel = loglevels.get(a, logger.INFO)
        elif o in [ '--loglevel']:
            loglevel = loglevels.get(a, logger.INFO)
        elif o in [ '--logfile']:
            logfile = a
        elif o in [ '--exclude']:
            exclude = a
        elif o in ['-w', '--workdir']:
            workdir = a
        elif o in ['-p', '--progress']:
            logprogress = True
            logconsole = False
        elif o in ['-c', '--console']:
            logconsole = True
            logprogress = False
        else:
            usage()
            return -1

    if merge and not outfn:
        usage()
        return -1
        
    if outfn and not outfn.endswith('.xlsx'):
        outfn += '-icd.xlsx'

    if logfile  is None:
        if outfn:
            logfile = '%s-iomgen.log' % outfn.rsplit('.', 1)[0]
        else:
            logfile = '%s-iomgen.log' % hfnamelist[0]

    os.chdir(workdir)

    logger.setup(filename=logfile, level=loglevel, console=logconsole, progress=logprogress)
    logger.info("STARTING Import")

    processIcd(sourcedirs, hfnamelist, exclude=exclude, outfilename=outfn, merge=merge)
    return 0

if __name__ == '__main__':
    sys.exit(main())
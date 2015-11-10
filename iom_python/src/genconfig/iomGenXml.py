import xlrd
import re
import sys
import getopt
    
from Cheetah.Template import Template
from lxml import etree
import iomGenCommon
import iomGenReadDD


import pdb
def excepthook(ex_cls, ex, tb):
    pdb.post_mortem(tb)
#sys.excepthook = excepthook



TEMPLATE_HEADER = '''
<IOMConfiguration HF="$model.identification.application" REV="$model.identification.revision" ICD="$model.identification.icd">
'''

TEMPLATE_CANIN = '''
<CanInput>
 #for $key in $model.can.messageKeys
  #set msg=$model.can.messages[$key]
  #if $msg.msgUsed
    <CanMessage id="$msg.msgid" messageName="$key" canId="$msg.msgCanID" rate="$msg.msgRate" length="$msg.msgLength">
        #for p in $model.can.datasets[$msg.msgid]
        <Parameter paramNameValue="$p.paramName" paramSize="$p.paramDatasize" paramType="$p.paramDatatype" paramNameStatus="$(p.paramName).Status" paramOffsetValue="$p.paramOffset" paramOffsetStatus="$p.paramOffsetStatus" paramDefault="$p.paramDefault" paramMin="$p.paramMin" paramMax="$p.paramMax">
            <source type="$p.sigType" message="$p.msgRef.msgid" offset="$p.sigByteOffset" lsb="$p.sigBitOffset" bits="$p.sigSize" access="$p.sigAccess" lsbvalue="$p.sigLsbValue"/>
        </Parameter>
        #end for
    </CanMessage>
  #end if
 #end for
</CanInput>
'''


TEMPLATE_AFDXIN = '''
<AfdxInput>
 #for $key in $model.afdx.messageKeys
  #set map=$model.afdx.messages[$key]
  #if $map.msgUsed
    <AfdxMessage id="$map.msgid" messageName="$key" portType="$map.portType" queueLength="$map.queueLength" portId="$map.portId" portName="$map.portName" rate="$map.msgValidityPeriod" length="$map.msgRxLength"/>
  #end if
 #end for

 #set $selectionSetName = "None"
 #for $source in $model.sources[0]
   #if $selectionSetName != $source.SelectionSet 
    #if $selectionSetName != "None"
    </SelectionSet>
    
    #end if
    #set $selectionSetName = $source.SelectionSet
    #if $source.SelectionCriteria == "SOURCE_HEALTH_SCORE"
    <SelectionSet selectionSetName="$selectionSetName" criteria="$source.SelectionCriteria" interval="$source.LockInterval">
    #else
    <SelectionSet selectionSetName="$selectionSetName" criteria="$source.SelectionCriteria">
    #end if
   #end if
    #if $source.SelectionCriteria == "LIC_PARAMETER"
     #for $dataset in $model.afdx.datasets.values():
      #if $dataset.has_key($source.LICParameter):
            #set $paramType         = $dataset[$source.LICParameter][0].paramDatatype
            #set $paramOffsetValue  = $dataset[$source.LICParameter][0].paramOffset
            #set $paramOffsetStatus = $dataset[$source.LICParameter][0].paramOffsetStatus
       #end if
     #end for
        <source name="$source.SourceName" order="$source.SelectionOrder" paramNameValue="$source.LICParameter" paramType="$paramType" paramOffsetValue="$paramOffsetValue" paramOffsetStatus="$paramOffsetStatus" expectedValue="$source.LICValue"/>
    #else
        <source name="$source.SourceName" order="$source.SelectionOrder"/>
    #end if
 #end for
 #if $selectionSetName != "None"
    </SelectionSet>   
 #end if
 
  
 #for $dsname in $model.afdx.datasets.keys()
    #set $dataset          = $model.afdx.datasets[$dsname]
    #set $selectionSetName = $dataset.values()[0][0].selectionSet
    
    <DataSet name="$dsname" selectionSetName="$selectionSetName">
        <Logic>
        #set $sources=$dataset.values()[0]
        #for $map in $sources
            <sourceLogic>
                #if $map.sselFreshness()
                <condition type="Freshness" message="$map.msgRef.msgid"/>
                #end if
                #if $map.sselMaskValue()
                #set $par=$map.sselMaskParams()
                #if $par is not None
                <condition type="MaskValue" message="$par.msgid" offset="$par.offset" mask="$par.mask" value="$par.value"/>
                #end if
                #end if
                #if $map.sselA664Fsb()
                <condition type="A664FS"    message="$map.msgRef.msgid" offset="$map.dsFsbOffset"/>    
                #end if
                #if $map.sselA429SSM_BCD()
                <condition type="A429SSM_BCD" message="$map.msgRef.msgid" offset="$map.sigByteOffset"/>    
                #end if
                #if $map.sselA429SSM_BNR()
                <condition type="A429SSM_BNR" message="$map.msgRef.msgid" offset="$map.sigByteOffset"/>    
                #end if
                #if $map.sselA429SSM_DIS()
                <condition type="A429SSM_DIS" message="$map.msgRef.msgid" offset="$map.sigByteOffset"/>    
                #end if
            </sourceLogic>
        #end for
        </Logic>
        #for $param in $dataset.values()
            #set $p = $param[0]
        <Parameter paramNameValue="$p.paramName" paramSize="$p.paramDatasize" paramType="$p.paramDatatype" paramNameStatus="$(p.paramName).Status" paramOffsetValue="$p.paramOffset" paramOffsetStatus="$p.paramOffsetStatus" paramDefault="$p.paramDefault" paramMin="$p.paramMin" paramMax="$p.paramMax">       
            #for $map in $param
            <source type="$map.sigType" message="$map.msgRef.msgid" offset="$map.sigByteOffset" access="$map.sigAccess" lsb="$map.sigBitOffset" bits="$map.sigSize" lsbvalue="$map.sigLsbValue"/>
            #end for
        </Parameter>
        #end for
    </DataSet>
 #end for
</AfdxInput>
'''

TEMPLATE_AFDXOUT='''
<AfdxOutput>
 #for $key in $model.afdx.messageKeys
  #set map=$model.afdx.messages[$key]
  #if $map.msgUsed
    <AfdxMessage id="$map.msgid" messageName="$key" portType="$map.portType" queueLength="$map.queueLength" portId="$map.portId" portName="$map.portName" rate="$map.msgRate" length="$map.msgLength"/>
  #end if
 #end for

 #for key in $model.afdx.datasets.keys()
    #set ds = $model.afdx.datasets[$key]
    <DataSet name="$key" dsOffset="$ds[0].dsDsOffset" fsbOffset="$ds[0].dsFsbOffset" messageId="$ds[0].msgRef.msgid" dsType="A664" dsA429Label="" dsA429SDI="" dsA429SSMType="">
        #for $p in $ds:
        <Parameter paramNameValue="$p.paramName" paramSize="$p.paramDatasize" paramType="$p.paramDatatype" paramNameStatus="$(p.paramName).Status" paramOffsetValue="$p.paramOffset" paramOffsetStatus="$p.paramOffsetStatus">
            <destination type="$p.sigType" message="$p.msgRef.msgid" offset="$p.sigByteOffset" access="$p.sigAccess" lsb="$p.sigBitOffset" bits="$p.sigSize" lsbvalue="$p.sigLsbValue"/>
        </Parameter>
        #end for
    </DataSet>
 #end for
</AfdxOutput>
'''

class Bunch(object):
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

def genXml(inputModel, outputModel, outfn):

    file = open(outfn, "w")

    
    if inputModel:
        tmpl = Template(TEMPLATE_HEADER, searchList=[{ "model" : inputModel }])
        file.write(tmpl.respond())
    elif outputModel:
        tmpl = Template(TEMPLATE_HEADER, searchList=[{ "model" : inputModel }])
        file.write(tmpl.respond())

    if inputModel:
        for tmplstr in (TEMPLATE_AFDXIN, TEMPLATE_CANIN):
            tmpl = Template(tmplstr, searchList=[{ "model" : inputModel }])
            file.write(tmpl.respond())

    if outputModel:
        for tmplstr in (TEMPLATE_AFDXOUT, ):
            tmpl = Template(tmplstr, searchList=[{ "model" : outputModel }])
            file.write(tmpl.respond())

    file.write("</IOMConfiguration>\n")

def usage():
    sys.stderr.write("Usage: iomGenXml excelicd [--indd inputdd] [--outdd outputdd] [-o outputfile]")

def main(arglist):

    # Parse command line arguments
    inputddfiles   =  []
    outputddfiles  = []
    xmlfile       = None

    opts, args = getopt.getopt(arglist, 'ho:', ['indd=', 'outdd=', 'output=', 'help'])

    for o, a in opts:
        if o in ['-h', '--help']:
            usage()
            return -1
        elif o in [ '--indd']:
            if a is not "":
                inputddfiles.append(a)
        elif o in [ '--outdd']:
            if a is not "":
                outputddfiles.append(a)
        elif o in [ '-o', '--output']:
            xmlfile = a
        else:
            usage()
            return -1

    if len(args) != 1:
        usage()
        return -1
        
    excelicdfile = args[0]

    if xmlfile is None:
        xmlfile = excelicdfile.rsplit(".", 1)[0] + '.xml'

    if len(inputddfiles) > 0:
        inputDD = iomGenReadDD.ddread(inputddfiles)
    else:
        inputDD = None

    if len(outputddfiles) > 0:
        outputDD = iomGenReadDD.ddread(outputddfiles)
    else:
        outputDD = None

    inputModel = iomGenCommon.MapReader(excelicdfile, dd=inputDD, msgonly=False, direction='input')
    outputModel = iomGenCommon.MapReader(excelicdfile, dd=outputDD, msgonly=False, direction='output')
    genXml(inputModel, outputModel, xmlfile)

    return 0


if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))
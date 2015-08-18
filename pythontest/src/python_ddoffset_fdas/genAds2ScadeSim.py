'''
Created on 18.11.2013

@author: tow, dk
'''

import os
from Cheetah.Template import Template

TOOL_ROOT = os.path.join('c:\\', 'TechSAT', 'TestFrameGen', 'lib', 'python')

CVT_TMPL = os.path.join(TOOL_ROOT, 'ScadeSimGen', 'cvt.tmpl')
CMP_TMPL = os.path.join(TOOL_ROOT, 'ScadeSimGen', 'cmp.tmpl')
IN_TMPL_SOLO = os.path.join(TOOL_ROOT, 'ScadeSimGen', 'scadeInNode_solo.tmpl')
IN_TMPL_SOLO_FDAS = os.path.join(TOOL_ROOT, 'ScadeSimGen', 'scadeInNode_solo_FDAS.tmpl')
OUT_TMPL_SOLO = os.path.join(TOOL_ROOT, 'ScadeSimGen', 'scadeOutNode_solo.tmpl')
IN_TMPL_DUO = os.path.join(TOOL_ROOT, 'ScadeSimGen', 'scadeInNode_duo.tmpl')
IN_TMPL_DUO_FDAS = os.path.join(TOOL_ROOT, 'ScadeSimGen', 'scadeInNode_duo_FDAS.tmpl')
OUT_TMPL_DUO = os.path.join(TOOL_ROOT, 'ScadeSimGen', 'scadeOutNode_duo.tmpl')
SIM_TMPL = os.path.join(TOOL_ROOT, 'ScadeSimGen', 'scadeSim.tmpl')
HEAD_TMPL = os.path.join(TOOL_ROOT, 'ScadeSimGen', 'scadeModelHeader.tmpl')
CSTRUCT_TMPL = os.path.join(TOOL_ROOT, 'ScadeSimGen', 'c_struct.tmpl')

class Bunch(object):
    def __init__(self, **kwds):
        self.__dict__.update(kwds)

def genDDMap(inputNamelist, outputNamelist, modelname, path):
    str = '<namelist model="%s">\n' % modelname
    if inputNamelist:
        for n in inputNamelist:
            str += '    <parameter offset="%(structoffset)s"  size="%(scadesize)s" elements="%(scadeelements)s" ' \
                   'type="%(scadetype)s" name="%(name)s"/>\n' % n
        str  += '</namelist>\n'
        open(os.path.join(path, modelname) + '.inddmap.xml', "w").write(str)
    
    if outputNamelist:
        str = '<namelist model="%s">\n' % modelname
        for n in outputNamelist:
            str += '    <parameter offset="%(structoffset)s"  size="%(scadesize)s" elements="%(scadeelements)s" ' \
                   'type="%(scadetype)s" name="%(name)s"/>\n' % n
        str += '</namelist>\n' 
        open(os.path.join(path, modelname) + '.outddmap.xml', "w").write(str)

def genCStruct(namelist, cvtname="", outname='', listname='pointlist'):
    tmpl = Template(
                file=CSTRUCT_TMPL,
                searchList=[{"cvtname"  : os.path.basename(cvtname),
                             "pointlist": namelist,
                             "listname" : listname}])
    s = tmpl.respond()
    open(outname +'.h', "w").write(s)

def genAds2Cvt(namelist, cvtname=""):
    tmpl = Template(file=CVT_TMPL, 
                searchList=[{ "cvtname"  : os.path.basename(cvtname), 
                              "pointlist": namelist }])
    s = tmpl.respond()
    open(cvtname +'.cvt', "w").write(s)

def genAds2Cmp(cmpname, cvtlist=[], simlist=[]):

    #if not simlist:
    #    simlist.append(Bunch(name="fake", length="-1"))

    tmpl = Template(file=CMP_TMPL, 
                searchList=[{ "cvtlist"  : cvtlist, "simlist": simlist}])
    s = tmpl.respond()
    open(cmpname +'.cmp', "w").write(s)

def genAds2ScadeInBlockSolo(namelist, modelname="", simname='', funcname='', namespace='', prefix='', outputlist=[], cvtname=''):
    #print outputlist
    tmpl = Template(file=IN_TMPL_SOLO, 
                searchList=[{"project"  : modelname, 
                             "function" : funcname,
                             "namespace": namespace,
                             "prefix"   : prefix,
                             "cvtname"  : cvtname,
                             "outlist"  : outputlist,
                             "pointlist": namelist
                }])
    s = tmpl.respond()
    open(simname +'.c', "w").write(s)

def genAds2ScadeInBlockSoloFDAS(namelist, modelname="", simname='', funcname='', namespace='', prefix='', outputlist=[], cvtname='', alertcvtname='', alertlist=[]):
    #print outputlist
    tmpl = Template(file=IN_TMPL_SOLO_FDAS, 
                searchList=[{"project"  : modelname, 
                             "function" : funcname,
                             "namespace": namespace,
                             "prefix"   : prefix,
                             "cvtname"  : cvtname,
                             "alertcvtname"  : alertcvtname,
                             "outlist"  : outputlist,
                             "pointlist": namelist,
                             "alertlist": alertlist
                }])
    s = tmpl.respond()
    open(simname +'.c', "w").write(s)

def genAds2ScadeOutBlockSolo(namelist, modelname="", simname='', funcname='', namespace='', prefix='', inputlist=[], cvtname=''):
    tmpl = Template(file=OUT_TMPL_SOLO, 
                searchList=[{"project"  : modelname, 
                             "function" : funcname,
                             "namespace": namespace,
                             "prefix"   : prefix,
                             "cvtname"  : cvtname,
                             "inlist"   : inputlist,
                             "pointlist": namelist
                }])
    s = tmpl.respond()
    open(simname +'.c', "w").write(s)
    
def genAds2ScadeInBlockDuo(namelist, modelname="", simname='', funcname='', namespace='', prefix='', outputlist=[], cvtname=''):
    #print outputlist
    tmpl = Template(file=IN_TMPL_DUO, 
                searchList=[{"project"  : modelname, 
                             "function" : funcname,
                             "namespace": namespace,
                             "prefix"   : prefix,
                             "cvtname"  : cvtname,
                             "outlist"  : outputlist,
                             "pointlist": namelist
                }])
    s = tmpl.respond()
    open(simname +'.c', "w").write(s)

def genAds2ScadeInBlockDuoFDAS(namelist, modelname="", simname='', funcname='', namespace='', prefix='', outputlist=[], cvtname='', alertcvtname='', alertlist=[]):
    #print outputlist
    tmpl = Template(file=IN_TMPL_DUO_FDAS, 
                searchList=[{"project"  : modelname, 
                             "function" : funcname,
                             "namespace": namespace,
                             "prefix"   : prefix,
                             "cvtname"  : cvtname,
                             "alertcvtname"  : alertcvtname,
                             "outlist"  : outputlist,
                             "pointlist": namelist,
                             "alertlist": alertlist
                }])
    s = tmpl.respond()
    open(simname +'.c', "w").write(s)

def genAds2ScadeOutBlockDuo(namelist, modelname="", simname='', funcname='', namespace='', prefix='', inputlist=[], cvtname=''):
    tmpl = Template(file=OUT_TMPL_DUO, 
                searchList=[{"project"  : modelname, 
                             "function" : funcname,
                             "namespace": namespace,
                             "prefix"   : prefix,
                             "cvtname"  : cvtname,
                             "inlist"   : inputlist,
                             "pointlist": namelist
                }])
    s = tmpl.respond()
    open(simname +'.c', "w").write(s)

def genAds2ScadeMain(namelist, modelname="", simname='', funcname='', prefix='', inputlist=[], outputlist=[], cvtname=''):
    tmpl = Template(file=SIM_TMPL, 
                searchList=[{"project"  : modelname, 
                             "function" : funcname,
                             "prefix"   : prefix,
                             "cvtname"  : cvtname,
                             "inlist"   : inputlist,
                             "outlist"  : outputlist,
                             "pointlist": namelist
                }])
    s = tmpl.respond()
    open(simname + '.c', "w").write(s)

def genAds2ScadeHeader(namelist, modelname="", simname='', prefix='', inputlist=[], outputlist=[], cvtname=''):
    tmpl = Template(file=HEAD_TMPL, 
                searchList=[{"project"  : modelname, 
                             "prefix"   : prefix,
                             "cvtname"  : cvtname,
                             "inlist"   : inputlist,
                             "outlist"  : outputlist,
                             "pointlist": namelist
                }])
    s = tmpl.respond()
    open(simname + '.h', "w").write(s)
    

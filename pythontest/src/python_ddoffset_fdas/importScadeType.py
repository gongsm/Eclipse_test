'''
Created on 18.11.2013

@author: tow, dk
'''

import os
import fnmatch

# only for testing
#import sys
#TOOL_LIB_ROOT = os.path.join('c:\\', 'TechSAT', 'TestFrameGen', 'lib', 'python')
#sys.path.append(TOOL_LIB_ROOT)

from exceptions import Exception
from lxml import etree
from Utilities.OrderedDict import OrderedDict



class Bunch(object):
    def __init__(self, **kwds):
        self.__dict__.update(kwds)


class XscadeReader(object):
    '''
    Implements functions to read SCADE xml files and generates an symbol tree,
    that can be used in C files or for CVT generation.
    '''
    def __init__(self, filename, rootpath=['./']):
        self.TypeDict = {'int': {"klass": "Basic"},
                         'short': {"klass": "Basic"},
                         'real': {"klass": "Basic"},
                         'bool': {"klass": "Basic"},
                         'char': {"klass": "Basic"}}
        self.OutputList = []
        self.InputList  = []
        self.ProcessedFilesSet = set()
        self.IncludedXscadeFilesSet = set()
        
        lfile = os.path.join('c:\\', 'TechSAT', 'TestFramegen', 'XscadeReader.log')
        self.logfile = open(lfile, "w")
        self.logfile.write('XscadeReader init. Filename: %s  Rootpath: %s.\n' % (filename, rootpath))

        self.rootpath = rootpath #[p.strip() for p in rootpath]
        fullname = self.find_file(filename)
        if fullname == None:
            s = 'Cannot find file %s under' % filename
            for p in self.rootpath:
                s+=' <' + p + '>'
                self.logfile.write(s)
            raise Exception(s)
        
        self.etprootpath = os.path.dirname(fullname)
        #self.getIncludedXscadeFiles()
            
        f = open(fullname, "r")
        self.tree = etree.parse(f)
        self.root = self.tree.getroot()
        self.nsmap = self.root.nsmap

    def findEtpFile(self):
        res = set() 
        for root, dirnames, filenames in os.walk(self.etprootpath):
            for filename in fnmatch.filter(filenames, '*.etp'):
                res.add(os.path.join(root, filename))
            break
        return res
        
    def getIncludedXscadeFiles(self):
        etpfile_set = self.findEtpFile()

        if len(etpfile_set) == 0:
            s = 'Connot find .etp file under %s.' % self.etprootpath
            self.logfile.write(s)
            raise Exception(s)
        if len(etpfile_set) > 1:
            s = 'Found more than one .etp file under %s.' % self.etprootpath
            self.logfile.write(s)
            raise Exception(s)
        
        etpfile = etpfile_set.pop()
        self.processEtpFile(etpfile)
        
    def processEtpFile(self, etpfile):
        try:
            f = open(etpfile, 'r')
        except:
            #f = open(self.find_file(os.path.basename(etpfile)))
            raise Exception('[Processing etp file]: Connot find etp file <%s>' % etpfile)
        
        etpcurrpath = os.path.abspath(os.path.dirname(etpfile))

        etptree = etree.parse(f)
        etproot = etptree.getroot()
        self.nsmap = etproot.nsmap

        folderroot = etproot.find(self.mktag('roots'))
        self.processFolder(folderroot, etpcurrpath)
        
    def processFolder(self, folderroot, etpcurrpath):
        for fo in folderroot.iterfind(self.mktag('Folder')):
            if fo.attrib['name'] == 'SCADE Libraries':
                continue
            self.processFolderElement(fo, etpcurrpath)
            
    def processFolderElement(self, folder, etpcurrpath):
        for fo in folder.iterfind(self.mktag(('elements', 'Folder'))):
            self.processFolder(fo, etpcurrpath)
        for fref in folder.iterfind(self.mktag(('elements', 'FileRef'))):
            self.processFileRef(fref, etpcurrpath)
            
    def processFileRef(self, fileref, etpcurrpath):
        filename = fileref.attrib['persistAs']
        if os.path.splitext(filename)[1] == '.xscade':
            self.IncludedXscadeFilesSet.add(filename)
        elif os.path.splitext(filename)[1] == '.etp':
            self.processEtpFile(os.path.join(etpcurrpath, filename))
        else:
            self.logfile.write('[Processing Etp file]: Unkonwn fileref <%s>' % fileref)
    
    def processProjectFile(self):
        extFunc = []
        if self.root.tag.endswith("Project"):
            for f in self.root.iterfind(self.mktag(('roots', 'Folder'))):
                if f.attrib['name'] == 'External Code':
                    for p in f.iterfind(self.mktag(('elements', 'FileRef', 'props', 'Prop'))):
                        if p.attrib['name'] =='@SCADE:IMPORTED_NODES':
                            val = p.find(self.mktag('value'))
                            extFunc.append(val.text)
        return extFunc

    def processNode(self):
        self.logfile.write("processNode\n")
        op = self.root
        try:
            if not op.tag.endswith("Operator"):
                decl = op.find(self.mktag('declarations'))
                op   = decl.find(self.mktag('Operator'))
                if op is None:
                    package = decl.find(self.mktag('Package'))
                    decl = package.find(self.mktag('declarations'))
                    op   = decl.find(self.mktag('Operator'))
        except:
            s = "Can't find toplevel operator in given Node. Please use an other file (e.g. <Model>TopLevel)"
            self.logfile.write(s)
            raise Exception(s)
               
        if op is None or op.attrib['kind'] != 'node':
            s = "Wrong Operator type. Operator of type 'node' expected."
            self.logfile.write(s)
            raise Exception(s)

        self.node = op.attrib['name']
        self.logfile.write("node: %s\n" % self.node)

        
        outputsdd = None
        o = op.find(self.mktag('outputs'))
        if o is None:
            self.logfile.write('[Process Node]: No outputs found')
        else:
            for v in o.iterfind(self.mktag('Variable')):
                if v.attrib['name'] == 'OutputsDD':
                    outputsdd = v
                    break
            if outputsdd is None:
                # Do nothing, if no variable with name 'OutputsDD' found.
                #self.processOutputs(o)
                self.logfile.write('[Process Node]: No OutputsDD found.')
            else:
                self.OutputList.append(self.processVariable(outputsdd))
        
        inputsdd = None
        i = op.find(self.mktag('inputs'))
        if i is None:
            self.logfile.write('[Process Node]: No inputs found')
        else:
            for v in i.iterfind(self.mktag('Variable')):
                if v.attrib['name'] == 'InputsDD':
                    inputsdd = v
            if inputsdd is None:
                # Do nothing, if no variable with name 'InputsDD' found.
                #self.processInputs(i)
                self.logfile.write('[Process Node]: No InputsDD found.')
            else:
                self.InputList.append(self.processVariable(inputsdd))

    def processFunction(self):
        self.logfile.write("processFunction\n")
        op = self.root
        if not self.root.tag.endswith("Operator"):
            decl = self.root.find(self.mktag('declarations'))
            op   = decl.find(self.mktag('Operator'))
        if op.attrib['kind'] != 'function':
            s = "Wrong Operator type. Operator of type 'function' expected."
            self.logfile.write(s)
            raise Exception(s)

        self.function = op.attrib['name']
        self.logfile.write("function: %s\n" % self.function)
        o = op.find(self.mktag('outputs'))
        if o is not None:
            self.processOutputs(o)
        
        i = op.find(self.mktag('inputs'))
        if i is not None:
            self.processInputs(i)

    def iter_xscadefiles(self):
        for path in self.rootpath:
            for root, dirs, files in os.walk(path):
                for f in files:
                    if f.endswith('.xscade'):
                        yield os.path.join(root, f)

    def find_file(self, filename):
        for path in self.rootpath:
            for root, dirs, files in os.walk(path):
                for f in files:
                    if f == filename:
                        return os.path.join(root, f)
        return None
    
    def findPackageDefFile(self, pkgName):
        self.logfile.write("findPackageDefFile: pkgName = %s\n" % pkgName)
        for path in self.rootpath:
            for root, dirs, files in os.walk(path):
                for f in files:
                    if f[-7:] == '.xscade':
                        self.tree = etree.parse(os.path.join(root, f))
                        self.root = self.tree.getroot()
                        self.nsmap = self.root.nsmap
                        package = self.root.find(self.mktag(('declarations','Package')))
#                        package = self.root.find(self.mktag(('declarations')))
                        
                        if package != None and package.attrib['name'] == pkgName:
                            self.logfile.write("Found package %s\n" % package)
                            return f
        
    def findTypeDef_internal(self, typename):
        self.logfile.write("findTypeDef_internal: typename = %s\n" % typename)
        for t in self.root.iterfind(self.mktag(('declarations', 'Type'))):
            if t.attrib['name'] == typename:
                self.logfile.write("%s found\n" % typename)
                return t
        for t in self.root.iterfind(self.mktag(('declarations', 'Package', 'declarations', 'Type'))):
            if t.attrib['name'] == typename:
                self.logfile.write("%s found\n" % typename)
                return t
        return None

    def findConstDef_internal(self, constname):
        self.logfile.write("findConstDef_internal: constname = %s\n" % constname)
        for t in self.root.iterfind(self.mktag(('declarations', 'Constant'))):
            if t.attrib['name'] == constname:
                self.logfile.write("%s found\n" % constname)
                return t
        for t in self.root.iterfind(self.mktag(('declarations', 'Package', 'declarations', 'Constant'))):
            if t.attrib['name'] == constname:
                self.logfile.write("%s found\n" % constname)
                return t
        return None

    def mktag_e(self, tag):
        try:
            prefix, name = tag.split(':')
        except:
            prefix = None
            name = tag
        if not self.nsmap:
            return "%s" % (name)
        return "{%s}%s" % (self.nsmap[prefix], name)
            
    def mktag(self, tag):
        path = ""
        if type(tag) == type(()):
            for t in tag:
                e = self.mktag_e(t)
                if path:
                    path += '/' + e
                else:
                    path = e
        else:
            path = self.mktag_e(tag)
        #self.logfile.write("mktag: path = %s\n" % path)
        return path


    def processOutputs(self, outputs):
        self.logfile.write("processOutputs")
        try:
            for var in outputs.iterfind(self.mktag('Variable')):
                self.OutputList.append(self.processVariable(var))
        except Exception as e:
            #print e
            pass
 
    def processInputs(self, inputs):
        self.logfile.write("processInputs")
        try:
            for var in inputs.iterfind(self.mktag('Variable')):
                self.InputList.append(self.processVariable(var))
        except:
            pass
        
    def processVariable(self, variable):
        varname = variable.attrib['name']
        typename, namespace = self.processType(variable[0])
        self.logfile.write("processVariable: varname = %s  typename = %s  namespace = %s" % (
                                                (varname, typename, namespace)))
        return (varname, typename, namespace)


    def processFile(self, filename, ispkg=False):
        '''
        Process xml file and look for type declarations
        '''
        if filename in self.ProcessedFilesSet:
            return
        #if not ispkg and os.path.basename(filename) not in self.IncludedXscadeFilesSet:
        #    return

        self.logfile.write("processFile: filename = %s ispkg = %d\n" % (filename, ispkg))

        if not os.path.dirname(filename):
            filename = self.find_file(filename)

        self.ProcessedFilesSet.add(filename)
        try:
            f = open(filename, "r")
        except:
            raise Exception('File %s not found.' % filename)

        self.tree = etree.parse(f)
        self.root = self.tree.getroot()
        self.nsmap = self.root.nsmap
        try:
            self.processPackage(self.root.find(self.mktag(('declarations','Package'))))
        except:
            pass
        try:
            self.processDeclarations_inner(self.root.find(self.mktag('declarations')))
        except:
            pass

    def processPackage(self, package):
        #print package.attrib['name']
        self.processDeclarations_inner(package.find(self.mktag('declarations')))


    def processDeclarations_inner(self, decl):
        try:
            for i in decl.iterfind(self.mktag('Constant')):
                self.processConstant(i)
            for i in decl.iterfind(self.mktag('Type')):
                self.processTypeDef(i)
        except Exception as e:
            print e
            pass
    
    def processTypeDef(self, typedef):
        struct = OrderedDict()
        enum = []
        typename = typedef.attrib['name']
        if typename=='OutputsPeerType':
            print typename
        definition = typedef.find(self.mktag('definition'))
        self.logfile.write("processTypeDef: typename = %s  definition = %s\n" % (
                                    (typename, definition)))
        content = definition[0]
        if content.tag == self.mktag('Struct'):
            fields = content[0]
            for f in fields.iterfind(self.mktag('Field')):
                res = self.processField(f)
                if len(res) == 2:
                    fname, tname = res
                    struct[fname] = tname
                elif len(res) == 4:
                    fname, tname, tparaname, tsize = res
                    if tname == 'Table':
                        tabletypename = "%s_%s" % (fname, tname)
                        struct[fname] = tabletypename
                        self.TypeDict[tabletypename] = {"klass": "Table", "type": tparaname, "size": tsize}
                    else:
                        print("Function not implemented. Please contact your administrator.")

            self.TypeDict[typename] = {"klass": "Struct", "type": struct}
        elif content.tag == self.mktag('Table'):
            tname = self.processType(content.find(self.mktag('type')))[0]
            size  = self.processSize(content.find(self.mktag('size')))
            self.TypeDict[typename] = {"klass": "Table", "type": tname, "size": size}
        elif content.tag == self.mktag('Enum'):
            values = content[0]
            for v in values.iterfind(self.mktag('Value')):
                enum.append(v.attrib['name'])    
            self.TypeDict[typename] = {"klass": "Enum", "type": enum}
        elif content.tag == self.mktag('NamedType'):
            ref = content
            tname = self.processType(definition)
            self.TypeDict[typename] = {"klass": "Type", "type": tname}
        else:
            print "Unknown Type tag: %s" % content.tag
            
    def processType(self, typetag):
        typeref = typetag.find(self.mktag(('NamedType', 'type', 'TypeRef')))
        tname = typeref.attrib['name']
        self.logfile.write("processType: typeref = %s  tname = %s\n" % (
                                    typeref, tname))
        l = tname.split('::')
        realname = l[-1]
        if len(l) > 1:
            packageName = l[0]
        else:
            packageName = ''
        self.logfile.write("test: realname = %s  packageName = %s\n" % (
                                    realname, packageName))
        testname = 'OutputsPeerType'
        if realname == testname:
            print realname
        if not self.TypeDict.has_key(realname):
            if len(l) > 1:
                # FIXME: package name is not always same as filename.
                try:
                    pkgDefFile = self.findPackageDefFile(packageName)
                    self.processFile(pkgDefFile, 1)
                    #self.processFile(packageName+'.xscade')
                except Exception as e:
                    # The file was not found, but we go on
                    self.logfile.write("processType: %s\n" % e)
                    print e
                    pass
            else:
                # Try to find type in the same file
                typedef = self.findTypeDef_internal(l[0])
                if typedef != None:
                    self.processTypeDef(typedef)
                else:
                    # Type not found, let's start a search for it
                    self.logfile.write('Referenced type %s is not defined in a package. ' \
                        'Try to find the definition file recursively from root path.\n' % tname)
                    files = self.iter_xscadefiles()
                    for f in files:
                        self.processFile(f)

        if not self.TypeDict.has_key(realname):
            self.logfile.write('Could not resolve %s. Going on.\n' % tname)
        return realname, packageName
    
    def processSize(self, sizetag):
        if sizetag[0].tag == self.mktag('IdExpression'):
            return self.processIdExpression(sizetag[0])
        else:
            return int(sizetag[0].attrib['value'])

        
    def processField(self, field):
        fname = field.attrib['name']
        ftype = field.find(self.mktag('type'))
        self.logfile.write('processField: fname = %s  ftype = %s\n' % (fname, ftype))

        if ftype.find(self.mktag('Table')) is not None:
            ttype = ftype.find(self.mktag(('Table', 'type')))
            size = self.processSize(ftype.find(self.mktag(('Table', 'size'))))
            return fname, 'Table', self.processType(ttype)[0], size

        else:
            return fname, self.processType(ftype)[0]
    
    def processIdExpression(self, idexptag):
        return self.processConstVarRef(idexptag.find(self.mktag(('path', 'ConstVarRef'))))
    
    def processConstVarRef(self, constVarRefTag):
        constTag = self.findConstDef_internal(constVarRefTag.attrib['name'])
        ctype, cvalue = self.processConstant(constTag)
        return cvalue
    
    def processConstant(self, constTag):
        ctype = constTag.find(self.mktag(('type', 'NamedType', 'type', 'TypeRef'))).attrib['name']
        # FIXME Support other types too
        cast = {'int' : int,
                'real': float}
        if ctype not in cast:
            self.logfile.write("Cannot process TypeRef %s. NOT YET IMPLEMENTED.\n" % constTag)
            return None, None
        try:
            cvalue = (cast[ctype])(constTag.find(self.mktag(('value', 'ConstValue'))).attrib['value'])
        except:
            cvalue = (cast[ctype])(constTag.find(self.mktag(('value', 'ConstValue'))).attrib['value'], 16)
        self.TypeDict[constTag.attrib['name']] = {'klass': 'Constant', 'type': ctype, 'value': cvalue}
        #self.logfile.write('processConstant: ctype = %s  cvalue = %s\n' % (ctype, cvalue))
        return ctype, cvalue
    
    scade2adsType = {
        "int": "int32",
        "real": "real32",
        "bool": "int32",
        "short": "int16",
        "char": "string"
    }
    
    scade2adsSize = {
        "int": 4,
        "real": 4,
        "bool": 4,
        "short": 2,
        "char": 1
    }

    scade2scadeSize = {
        "int": 4,
        "real": 4,
        "bool": 4,
        "short": 2,
        "char": 1
    }
    
    struct_alignment = 4

    def align(self, offset, size):
        # round up to the next multiple of size
        return (offset + size - 1) & ~(size - 1)

    def mkNameList(self, nlist, prefix, typename, cvt_direction, offset = None):
        '''
        return prefix.field.field... , "int", 100
        '''
        if offset is None:
            offset = Bunch(val=0)

        typedef = self.TypeDict[typename]

        while typedef["klass"] == "Type":  # type reference
            typedef = self.TypeDict[typedef["type"][0]]

        if typedef["klass"] == "Struct":
            offset.val = self.align(offset.val, self.struct_alignment)
            for fieldname, fieldtype in typedef["type"].items():
                self.mkNameList(nlist, prefix + '.' + fieldname, fieldtype, cvt_direction, offset=offset)

        elif typedef["klass"] == "Table":
            scade_type = typedef["type"]
            scade_elemsize = self.scade2scadeSize[scade_type]
            scade_size = scade_elemsize * typedef["size"]
            ads2_type = self.scade2adsType[scade_type]
            ads2_size = self.scade2adsSize[scade_type]
            offset.val = self.align(offset.val, scade_elemsize)
           
            nlist.append({
                    "name":         prefix, 
                    "scadetype":    scade_type,
                    "scadesize":    scade_elemsize,
                    "structoffset": offset.val,
                    "type":         ads2_type, 
                    "elements":     1 if ads2_type == "string" else typedef["size"],
                    "datasize":     typedef["size"],
                    "direction":    cvt_direction,
                    "scadeelements": typedef["size"]
                    }) 
            offset.val += scade_size
            
        elif typedef["klass"] == "Basic":
            scade_type = typename
            scade_elemsize = self.scade2scadeSize[scade_type]
            scade_size = scade_elemsize * 1
            ads2_type = self.scade2adsType[scade_type]
            ads2_size = self.scade2adsSize[scade_type]
            offset.val = self.align(offset.val, scade_elemsize)

            nlist.append({
                    "name":         prefix, 
                    "scadetype":    typename,
                    "scadesize":    scade_elemsize,
                    "structoffset": offset.val,
                    "type":         ads2_type,
                    "elements":     1, 
                    "datasize":     ads2_size,
                    "direction":    cvt_direction,
                    "scadeelements": 1
            })
            offset.val += scade_size

        elif typedef["klass"] == "Constant":
            scade_type = typename
            scade_elemsize = self.scade2scadeSize[scade_type]
            scade_size = scade_elemsize * 1
            ads2_type = self.scade2adsType[scade_type]
            ads2_size = self.scade2adsSize[scade_type]
            offset.val = self.align(offset.val, scade_elemsize)
            
            nlist.append({
                    "name":         prefix, 
                    "scadetype":    typename,
                    "scadesize":    scade_elemsize,
                    "structoffset": offset.val,
                    "type":         ads2_type,
                    "elements":     1, 
                    "datasize":     ads2_size,
                    "direction":    cvt_direction,
                    "scadeelements": 1
            })

            offset.val += scade_size
            
        elif typedef["klass"] == "Enum":
            scade_type = 'int'
            scade_elemsize = self.scade2scadeSize[scade_type]
            scade_size = scade_elemsize * 1
            ads2_type = self.scade2adsType[scade_type]
            ads2_size = self.scade2adsSize[scade_type]
            offset.val = self.align(offset.val, scade_elemsize)
            
            nlist.append({
                    "name":         prefix, 
                    "scadetype":    scade_type,
                    "scadesize":    scade_elemsize,
                    "structoffset": offset.val,
                    "type":         ads2_type,
                    "elements":     1, 
                    "datasize":     ads2_size,
                    "direction":    cvt_direction,
                    "scadeelements": 1
            })

            offset.val += scade_size
            
        else:
            print "Unknown type definition %s" % typedef["klass"]
            
# Testing
#if __name__ == '__main__':
    #iReader = XscadeReader('ModelInput.xscade', ['C:\\Work\\C919_DS\\07_Tests\\707_Synoptics\\SUT\\20141128_Synoptics_Release0.3\\Behaviour\\SynopticUA'])
    #iReader = XscadeReader('ModelInput.xscade', ['C:\\Work\\C919_DS\\04_Sources\\410_DisplayManagerHDD\\head\\Model\\Behaviour\\DisplayManagerHDD'])
    #iReader = XscadeReader('ModelInput.xscade', ['C:\\Work\\C919_DS\\04_Sources\\412_HDD\\41210_PFD\\head\\Model\\Behaviour'])
            
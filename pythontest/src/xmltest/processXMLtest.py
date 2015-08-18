import sys
from lxml import etree




class Parameter():
        def __init__(self, xp, baseoffset=0):
            self.name      = xp.attrib["name"]
            self.key       = self.name.split('.', 1)[-1]
            self.type      = xp.attrib["type"].strip().upper()
            self.offset    = int(xp.attrib["offset"]) + baseoffset
            self.elements  = int(xp.attrib["elements"])
            if self.type == "REAL":
                 self.type = "FLOAT"
            if not self.type in ("FLOAT", "INT", "BOOL", "ENUM", "CHAR"):
                raise Exception, "Unsupported type in DD: %s (%s)" % (self.type, self.name)
            if (self.elements > 1 and self.type != "CHAR"):
                 raise Exception, "Unsupported type in DD: array of %s (%s)" % (self.type, self.name)
                 

params = {}

xmltree = etree.parse('E:/python_test/xmltest/test.inddmap.xml')


root = xmltree.getroot()
print root.nsmap
print root.attrib
print root.tag

#for t in root:
#        print t.tag
s = root.attrib.get("offset")

print root.tag

for xmlparam in root.iterfind("parameter"):
        
        
#   print xmlparam
#    try:
        param = Parameter(xmlparam)
 #   print param
        if param.key in params:
                print "duplicate parameter"
        else:
                params[param.key] = param
#print params


 #   except Exception, msg:
#        logerr(filename, msg)
#    continue
    


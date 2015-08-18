import iomGenXmlV2
import iomGenVxWV2
import iomGenBinV2
import sys
import os
import getopt


def usage():
    print 'Usage: iomGenConfig [--littleendian|--bigendian] [--steps XBV] [--sol pseudoPort|hddPort|imaCVT] [--indd modelinputdd] [--outdd modeloutputdd] -o outputdir --app appname excelicd'
    sys.exit(1)

def main():
    # Parse command line arguments
    inputddfiles  = []
    outputddfiles = []
    outputdir     = None
    appname       = None
    endian          = '--xxendian'
    steps           = 'XBV'
    sys.argv = [sys.argv[0],'--steps','XV','--bigendian','--indd','F:/workspace/pythontest/src/genconf661/A661.inddmap.xml','--outdd', 'F:/workspace/pythontest/src/genconf661/A661.outddmap.xml','-o','F:/workspace/pythontest/src/genconf661','--app','A661SRVIOM','F:/workspace/pythontest/src/genconf661/A661SRVIOM.xlsx']
    opts, args = getopt.getopt(sys.argv[1:], 'ho:', \
                            ['littleendian', 'bigendian', 'xxendian', 'steps=', 'indd=', 'outdd=', 'outdir=', 'app=', 'help'])

    for o, a in opts:
        if o in ['-h', '--help']:
            usage()
        elif o in ['--littleendian', '--bigendian']:
            endian = o
        elif o in [ '--indd']:
            inputddfiles.append(a)
        elif o in [ '--outdd']:
            outputddfiles.append(a)
        elif o in [ '-o', '--outdir']:
            outputdir = a
        elif o in [ '-a', '--app']:
            appname = a
        elif o in [ '--steps']:
            steps = a
        else:
            usage()
            sys.exit(1)

    if len(args) != 1:
        usage()

    excelfile = args[0]
    
    if inputddfiles is [] and outputddfiles is []:
        usage()
    
    if outputdir is None or appname is None:
        usage()
    
    basename = os.path.basename(excelfile).rsplit('.', 1)[0]

    if not os.path.isdir(outputdir):
        os.mkdir(outputdir)

    xmlfile  = os.path.join(outputdir, basename + '.xml')

    if 'X' in steps:
        arglist = []
        for x in inputddfiles:
            arglist += ['--indd', x] 
        for x in outputddfiles:
            arglist += ['--outdd', x] 
        if iomGenXmlV2.main(arglist + ['-o', xmlfile, excelfile]) != 0:
            print "iomGenXml failed"
        else:
            print "iomGenXml OK"
    
    if 'B' in steps:
        if iomGenBinV2.main(['--littleendian', xmlfile, outputdir]) != 0:
            print "iomGenBIN --littleendian failed"
        else:
            print "iomGenBIN --littleendian OK"

        if iomGenBinV2.main(['--bigendian', xmlfile, outputdir]) != 0:
            print "iomGenBIN --bigendian failed"
        else:
            print "iomGenBIN --bigendian OK"
    
    if 'V' in steps:
        if iomGenVxWV2.main([xmlfile, appname, outputdir]) != 0:
            print "iomGenVXW failed"
        else:
            print "iomGenVXW OK"
    
if __name__ == "__main__":
    sys.exit(main())
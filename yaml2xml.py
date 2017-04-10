#!/usr/bin/env python
"""
 @author : phil estival flint at forge dot systems

 An xml to yaml converter and vice versa

 notes :
 - Xml node attributes becomes the element '_' in the produced yaml
   and any ':' in xml attributes is converted to '@' in yml
   they are injected back to normal  when yml->xml
"""

import sys, re, types, yaml
from xml.dom import minidom, Node

NonWhiteSpacePattern = re.compile('\S')
def isAllWhiteSpace(text):
    return not NonWhiteSpacePattern.search(text)

class Yaml2xml:

    def __init__(self):
        pass

    def convertYaml2Xml(self,content):
        '''
        Convert a YAML input to XML ouput.
        attributes goes in a dictionnary prefixed by _
        '''
        inobj = yaml.safe_load(content)
        out = []
        L = 0
        self.convertYam2Xml(inobj, L, out)
        return "".join(out)

    #
    # Convert an XML document to YAML.
    #
    def convertXml2Yaml(self,doc):
        out = []
        L = 0
        root = doc.childNodes[0]
        self.convertXml2YamlAux(root, L, out)
        return "".join(out)


    def writeAttributes(self,D,L,out):
        for K,V in D.iteritems() :
            K=K.replace('@',':')
            out.append('\n%s%s="%s"'%("  "*L,str(K),str(V)))

    def convertYam2Xml(self,D,L,out):
        if type(D) is types.DictType:
            for K,V in D.iteritems() :
                if(K=="_"): # step back
                    out[-1]=out[-1][:-2]
                    self.writeAttributes(V,L,out)
                    out.append( ">\n")
                else:
                    out.append( "%s<%s>\n" % ("  "*L,K))
                    self.convertYam2Xml(V,1+L,out)
                    out.append( "%s</%s>\n" % ("  "*L,K))

        elif type(D) is types.ListType:
            for K in D:
                self.convertYam2Xml(K, 1+L, out)
        else:
            if(D) : out.append('%s  %s\n' %("  "*L, D))

    def convertXml2YamlAux(self,obj, L, out):
        sep='- '
        if L == 0: sep=''
        out.append('%s%s%s: ' % (L*'  ', sep, obj.nodeName) )
        # Dump the attributes.
        attrs = obj.attributes
        if attrs.length > 0:
            out.append('\n')
            out.append('%s- _: { '%((1+L)*'  '))
            for idx in range(attrs.length):
                attr = attrs.item(idx)
                attr.name = attr.name.replace(':','@')
                out.append("%s: '%s' " % (attr.name, attr.value))
                if(idx<attrs.length-1): out.append(", ")
            out.append('}')

        text = []
        if(len(obj.childNodes)==0):
            return
        else:
            for child in obj.childNodes:
                s = str(child.nodeValue)
                if child.nodeType == Node.COMMENT_NODE \
                  and not isAllWhiteSpace(s):
                    s=re.sub(r'\n\s+','\n'+((1+L)*'  ')+'# ',s)
                    out.append("\n%s# %s" %((1+L)*'  ',s))

                if child.nodeType == Node.TEXT_NODE \
                  and not isAllWhiteSpace(s):
                    s="".join(s)
                    if '*' in s or s.startswith('!'):
                        out.append("'%s'" %s)
                    else:
                        out.append("%s" %s)

                if child.nodeType == Node.ELEMENT_NODE:
                   out.append('\n')
                   self.convertXml2YamlAux(child, 1+L, out)


USAGE_TEXT = """
    Convert a file from YAML to XML or XML to YAML and write it to stdout.

    Usage: python yaml2xml <option> <in_file>

    Options:
        -y2x    Convert YAML file to XML document.
        -x2y    Convert XML document to YAML.
        -roundtrip    XML > YML > XML.
    """

def usage():
    print USAGE_TEXT
    sys.exit(-1)


def main():
    args = sys.argv[1:]

    if len(args) != 2: usage()

    option = args[0]
    infileName = args[1]

    y2x = Yaml2xml()

    if option == '-y2x':
        with open(infileName) as dat:
            content=dat.read()
        sys.stdout.write(
            y2x.convertYaml2Xml(content)
           )
    elif option == '-x2y':
        doc = minidom.parse(infileName)
        sys.stdout.write(
            y2x.convertXml2Yaml(doc)
        )
    elif option == '-roundtrip':
        doc = minidom.parse(infileName)
        y = Yaml2xml().convertXml2Yaml(doc)
        x = Yaml2xml().convertYaml2Xml(y)
        doc = minidom.parseString(x)
        print 'alright!'
    else:
        usage()

if __name__ == '__main__': main()

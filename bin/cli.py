#!/usr/bin/env python
"""
 @author : phil estival flint at forge dot systems

 An xml to yaml converter and vice versa

 notes :
 - Xml node attributes becomes the element '_' in the produced yaml
   and any ':' in xml attributes is converted to '@' in yml
   they are injected back to normal  when yml->xml
"""

import sys
from xml.dom import minidom
from yaml2xml.yaml2xml import Yaml2xml


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

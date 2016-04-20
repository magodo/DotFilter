#!/usr/bin/env python
# -*- coding: utf-8 -*-

#########################################################################
# Author: Zhaoting Weng
# Created Time: Sun 18 Oct 2015 01:12:45 PM CST
# File Name: dot_pair.py
# Description:
#########################################################################

class dot_pair(object):
    """
    This class is for parsing each line of dot file and get a dot_pair instnace.
    """
    def __init__(self, ID):
        """
        Private init function.

        :param int ID:          Id number to identify each pair
        """
        super(dot_pair, self).__init__()
        self.ID = ID
        self.isNode = False
        self.sourceNode = ""
        self.destNode = ""
        self.attr = {}

    def __getAttr(self, line):
        """
        Parse attribute of each line.

        :param str line:        Content of line
        """
        if not "[" in line:
            return
        attrs = line[line.index("[")+1:line.index("]")].split(',')
        for attr in attrs:
            attr = attr.strip()
            key, sep, value = attr.partition("=")
            key = key.strip()
            value = value.strip("\" \t")   # Strip '"'(double quote) and ' '(space)
            self.attr[key] = value

    def __checkIsNode(self, line):
        """
        Check if this line defines a node.

        :param str line:        Content of line
        """
        if not "->" in line:
            self.isNode = False
        else:
            self.isNode = True

    def __getSourceNode(self, line):
        """
        Parse each line and get source node.

        :param str line:        Content of line
        """
        line = line[:line.index("->")]
        self.sourceNode = line.strip("\" \t")

    def __getDestNode(self, line):
        """
        Parse each line and get destination node.

        :param str line:        Content of line
        """
        startIndex = line.index('->') + len('->')
        endIndex = len(line)
        if ";" in line:
            endIndex = line.index(';')
        if "[" in line:
            endIndex = line.index('[')
        line = line[startIndex:endIndex]
        self.destNode = line.strip("\" \t")

    def getSourceNode(self):
        """
        Return the source node of this node pair.
        """
        return self.sourceNode

    def getDestNode(self):
        """
        Return the dest node of this node pair.
        """
        return self.destNode

    def getPairID(self):
        """
        Return the ID of this dot pair.
        """
        return self.ID

    def getAttr(self):
        """
        Return attribute dictionary.
        """
        return self.attr

    def parseLine(self, line):
        """
        Parse line of dot file.

        :param str line:        Content of line
        :param bool    :        True if this line defines dot pair; Otherwise return 0
        """
        line = line.strip()
        self.__checkIsNode(line)
        if not self.isNode:
            return False
        self.__getAttr(line)
        self.__getSourceNode(line)
        self.__getDestNode(line)
        return True

if __name__ == "__main__":
    line1 = 'execute -> compare [shape=polygon, skew=0, distortion = 0.0, peripheries=3, color=".7 .3 1.0"]'
    line2 = '"lazy.target"->"ovip-core-ssw-security-efsv.service" [color="green"];'
    for line in [line1, line2]:
        inst = dot_pair()
        if inst.parseLine(line):
            print "Source: %s\nDest: %s" %(inst.getSourceNode(),inst.getDestNode())
            attrs = inst.getAttr()
            for attr in attrs:
                print "\tKey: %s\n\tValue: %s\n"%(attr, attrs[attr])


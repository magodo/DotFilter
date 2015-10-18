#!/usr/bin/env python
# -*- coding: utf-8 -*-

#########################################################################
# Author: Zhaoting Weng
# Created Time: Sun 18 Oct 2015 06:49:21 PM CST
# File Name: viewer.py
# Description:
#########################################################################

import parser
import os
import copy

def view(inputFile, fromNode = "", toNode = "", filters = [], outputFile = ""):
    """
    View dot file.

    :parapm str inputFile:      Input dot file
    :param str fromNode:        From which node does this viewer will present
    :param str toNode:          To which node does this viewer will present
    :param list filters:        List of filter option to just show nodes with these attributes
    :param str outputFile:      Output dot file
    """

    pairFull = set()

    # Parse file
    cnt = 1
    with open(inputFile, 'rU') as f:
        for line in f:
            dotPair = parser.DotPair(cnt)
            if dotPair.parseLine(line):
                pairFull.add(dotPair)
                cnt += 1


    pairShowTo = __getToPair(pairFull, toNode)
    pairShowFrom = __getFromPair(pairFull, fromNode)
    pairShow = pairShowFrom.intersection(pairShowTo)
    content = __dotReConstructor(pairShow)
    __populateDotFile(content, outputFile)

def __getFromPair(pairFull, fromNode):
    """
    Get set of pair which are on path from "From Node". If "From Node" is not set, return full set of DotPair.

    :param set pairFull:        Full set of DotPair
    :param str fromNode:        From which node does this viewer will present
    :return set:                Set of DotPair on path to "To Node"
    """
    if not fromNode:
        print "From each node..."
        return pairFull
    nodeSource = {fromNode}
    pairTemp = set()
    pairShow = set()
    while nodeSource:
        pairShow_ori = copy.copy(pairShow)
        pairTemp = copy.copy(pairFull)
        for pair in pairFull:
            if pair.getSourceNode() in nodeSource:
                pairShow.add(pair)
                pairTemp.remove(pair)
        pairFull = pairTemp
        nodeSource = {pair.getDestNode() for pair in pairShow.difference(pairShow_ori)}
    return pairShow

def __getToPair(pairFull, toNode):
    """
    Get set of pair which are on path to "To Node". If "To Node" is not set, return full set of DotPair.

    :param set pairFull:        Full set of DotPair
    :param str toNode:          To which node does this viewer will present
    :return set:                Set of DotPair on path to "To Node"
    """
    if not toNode:
        print "To each node..."
        return pairFull
    nodeDest = {toNode}
    pairTemp = set()
    pairShow = set()
    while nodeDest:
        pairShow_ori = copy.copy(pairShow)
        pairTemp = copy.copy(pairFull)
        for pair in pairFull:
            if pair.getDestNode() in nodeDest:
                pairShow.add(pair)
                pairTemp.remove(pair)
        pairFull = pairTemp
        nodeDest = {pair.getSourceNode() for pair in pairShow.difference(pairShow_ori)}
    return pairShow

def __dotReConstructor(pairShow):
    """
    Re-construct dot file based on all dot pairs to show.

    :param set pairShow:        Set of DotPair
    :return str:                Re-constructed content of dot file
    """
    content = "digraph G{\n"
    for pair in pairShow:
        content += "    %s -> %s" %(pair.getSourceNode(), pair.getDestNode())
        dictAttr = pair.getAttr()
        if dictAttr:
            content += " ["
            for key in dictAttr:
                content += "%s = \"%s\", " %(key, dictAttr[key])
            content = content[:-2] + "]"
        content += "\n"
    content += "}\n"
    return content

def __populateDotFile(content, outputFile):
    """
    Populate dot file.

    :param str content:         Re-constructed content of dot file
    :param str outputFile:     Output dot file
    """
    with open(outputFile, "w") as f:
        f.write(content)
    print "Dot file is populated as: %s"%os.path.realpath(outputFile)


if __name__ == "__main__":
    view("demo.dot", toNode = "make_string", fromNode = "main", outputFile = "./output.dot")






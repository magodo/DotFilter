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
    # Parse file
    pairFull = set()
    ID = 1
    with open(inputFile, 'rU') as f:
        for line in f:
            dotPair = parser.DotPair(ID)
            if dotPair.parseLine(line):
                pairFull.add(dotPair)
                ID += 1

    pairShowTo = __getToPair(pairFull, toNode, filters)
    pairShowFrom = __getFromPair(pairFull, fromNode, filters)
    pairShow = pairShowFrom.intersection(pairShowTo)
    # Reconstruct dot file
    content = __dotReConstructor(pairShow)
    __populateDotFile(content, outputFile)

def __getFromPair(pairFull, fromNode, filters):
    """
    Get set of pair which are on path from "From Node" and conform to filters.

    :param set pairFull:        Full set of DotPair
    :param str fromNode:        From which node does this viewer will present
    :param list filters:        List of filter option to just show nodes with these attributes
    :return set:                Set of DotPair on path to "To Node"
    """
    pairShow = set()
    pairTemp = set()
    # All path
    if not fromNode:
        print "From each node..."
        for pair in pairFull:
            # Check filter
            if (filters and __isFilteredDot(pair, filters)) or (not filters):
                pairShow.add(pair)
        return pairShow
    # Only path from 'fromNode'
    nodeSource = {fromNode}
    while nodeSource:
        pairShow_ori = copy.copy(pairShow)
        pairTemp = copy.copy(pairFull)
        for pair in pairFull:
            # Check filter
            if (filters and __isFilteredDot(pair, filters)) or (not filters):
                if pair.getSourceNode() in nodeSource:
                    pairShow.add(pair)
                    pairTemp.remove(pair)
        pairFull = pairTemp
        nodeSource = {pair.getDestNode() for pair in pairShow.difference(pairShow_ori)}
    return pairShow

def __getToPair(pairFull, toNode, filters):
    """
    Get set of pair which are on path to "To Node" and conform to filters.

    :param set pairFull:        Full set of DotPair
    :param str toNode:          To which node does this viewer will present
    :param list filters:        List of filter option to just show nodes with these attributes
    :return set:                Set of DotPair on path to "To Node"
    """
    pairShow = set()
    pairTemp = set()
    # All path
    if not toNode:
        print "To each node..."
        for pair in pairFull:
            # Check filter
            if (filters and __isFilteredDot(pair, filters)) or (not filters):
                pairShow.add(pair)
        return pairShow
    # Only path to 'toNode'
    nodeDest = {toNode}
    pairTemp = set()
    pairShow = set()
    while nodeDest:
        pairShow_ori = copy.copy(pairShow)
        pairTemp = copy.copy(pairFull)
        for pair in pairFull:
            # Check filter
            if (filters and __isFilteredDot(pair, filters)) or (not filters):
                if pair.getDestNode() in nodeDest:
                    pairShow.add(pair)
                    pairTemp.remove(pair)
        pairFull = pairTemp
        nodeDest = {pair.getSourceNode() for pair in pairShow.difference(pairShow_ori)}
    return pairShow

def __isFilteredDot(pair, filters):
    """
    Check if a certain DotPair in filter.

    :param DotPair:             DotPair to be checked
    :param list filters:        List of filter option to just show nodes with these attributes
    :return bool:               True if dot is confronted to filter. Else, return False
    """
    __DictAttr__ = {"conflict": "red", "dependency": "green", "require": "grey66", "order": "black"}
    dictAttr = pair.getAttr()
    if "color" not in dictAttr:
        color = "black"
    else:
        color = dictAttr["color"]
    filters = [__DictAttr__[case] for case in filters]
    if color not in filters:
        return False
    return True

def __dotReConstructor(pairShow):
    """
    Re-construct dot file based on all dot pairs to show.

    :param set pairShow:        Set of DotPair
    :return str:                Re-constructed content of dot file
    """
    content = "digraph G{\n"
    for pair in pairShow:
        content += "    \"%s\"->\"%s\"" %(pair.getSourceNode(), pair.getDestNode())
        dictAttr = pair.getAttr()
        if dictAttr:
            content += " ["
            for key in dictAttr:
                content += "%s=\"%s\", " %(key, dictAttr[key])
            content = content[:-2] + "]"
        content += ";\n"
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


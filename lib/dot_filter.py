#!/usr/bin/env python
# -*- coding: utf-8 -*-

#########################################################################
# Author: Zhaoting Weng
# Created Time: Sun 18 Oct 2015 06:49:21 PM CST
# File Name: dot_filter.py
# Description:
#########################################################################

import dot_pair
import os
import copy
import re
import logging
import sys

logger = logging.getLogger("My Log")
logger.setLevel(logging.INFO)
sh = logging.StreamHandler(sys.stdout)
sh.setLevel(logging.DEBUG)
logger.addHandler(sh)

class dot_filter(object):
    '''
    This class is for filtering dot files.
    '''

    def __init__(self, origin = ""):
        '''
        Private init function.

        :param str origin:              Used for determine the origin of the dot file. Current supported: bitbake, systemd
        '''
        super(dot_filter, self).__init__()
        self.origin = origin

    def filt(self, inputFile, fromNode = "", toNode = "", filters = [], outputFile = ""):
        """
        filter dot file.

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
                dotPair = dot_pair.dot_pair(ID)
                if dotPair.parseLine(line):
                    pairFull.add(dotPair)
                    ID += 1

        pairShowTo = self.__getToPair(pairFull, toNode, filters)
        pairShowFrom = self.__getFromPair(pairFull, fromNode, filters)
        pairShow = pairShowFrom.intersection(pairShowTo)
        # Reconstruct dot file
        content = self.__dotReConstructor(pairShow)
        self.__populateDotFile(content, outputFile)

    def __getFromPair(self, pairFull, fromNode, filters):
        """
        Get set of pair which are on path from "From Node" and conform to filters.

        :param set pairFull:        Full set of DotPair
        :param str fromNode:        From which node does this viewer will present
        :param list filters:        List of filter option to just show nodes with these attributes
        :return set:                Set of DotPair on path to "To Node"
        """
        logger.debug("%s.__getFromPair: ENTER"%self.__class__)
        pairShow = set()

        if not fromNode:
            # All path
            logger.info("From each node...")
            for pair in pairFull:
                # Check filter
                if (filters and self.__isFilteredDot(pair, filters)) or (not filters):
                    pairShow.add(pair)
        else:
            # Only path from 'fromNode'
            nodeSource = set()
            try:
                p = re.compile(fromNode.encode('string-escape'))
            except re.error as e:
                print "\nYour REGEXP seems not correct!\n"
                raise e
            for pair in pairFull:
                if p.match(pair.getSourceNode()):
                    nodeSource.add(pair.getSourceNode())
            logger.debug("From node are: %s" %(repr(nodeSource)))
            while nodeSource:
                pairShow_ori = copy.copy(pairShow)
                pairTemp = copy.copy(pairFull)
                for pair in pairFull:
                    # Check filter
                    if (filters and self.__isFilteredDot(pair, filters)) or (not filters):
                        if pair.getSourceNode() in nodeSource:
                            pairShow.add(pair)
                            pairTemp.remove(pair)
                pairFull = pairTemp
                nodeSource = {pair.getDestNode() for pair in pairShow.difference(pairShow_ori)}
        logger.debug("%s.__getFromPair: LEAVE"%self.__class__)
        return pairShow

    def __getToPair(self, pairFull, toNode, filters):
        """
        Get set of pair which are on path to "To Node" and conform to filters.

        :param set pairFull:        Full set of DotPair
        :param str toNode:          To which node does this viewer will present
        :param list filters:        List of filter option to just show nodes with these attributes
        :return set:                Set of DotPair on path to "To Node"
        """
        logger.debug("%s.__getToPair: ENTER"%self.__class__)
        pairShow = set()
        if not toNode:
            # All path
            logger.info("To each node...")
            for pair in pairFull:
                # Check filter
                if (filters and self.__isFilteredDot(pair, filters)) or (not filters):
                    pairShow.add(pair)
        else:
            # Only path to 'toNode'
            nodeDest = set()
            try:
                p = re.compile(toNode.encode('string-escape'))
            except re.error as e:
                print "\nYour REGEXP seems not correct!\n"
                raise e
            for pair in pairFull:
                if p.match(pair.getDestNode()):
                    nodeDest.add(pair.getDestNode())
            logger.debug("To node are: %s" %(repr(nodeDest)))
            while nodeDest:
                pairShow_ori = copy.copy(pairShow)
                pairTemp = copy.copy(pairFull)
                for pair in pairFull:
                    # Check filter
                    if (filters and self.__isFilteredDot(pair, filters)) or (not filters):
                        if pair.getDestNode() in nodeDest:
                            pairShow.add(pair)
                            pairTemp.remove(pair)
                pairFull = pairTemp
                nodeDest = {pair.getSourceNode() for pair in pairShow.difference(pairShow_ori)}
        logger.debug("%s.__getToPair: LEAVE"%self.__class__)
        return pairShow

    def __isFilteredDot(self, pair, filters):
        """
        Check if a certain DotPair in filter.

        :param DotPair:             DotPair to be checked
        :param list filters:        List of filter option to just show nodes with these attributes
        :return bool:               True if dot is confronted to filter. Else, return False
        """
        if self.origin == 'systemd':
            __DictAttr__ = {"conflicts": "red", "after": "green", "wants": "grey66", "requires": "black", "requisite": "darkblue"}
            dictAttr = pair.getAttr()
            color = dictAttr["color"]   # each pair(X->Y) has attribute 'color' in systemd generated dot file
            filters = [__DictAttr__[case] for case in filters]
            if color not in filters:
                return False
            return True

        if self.origin == 'bitbake':
            __DictAttr__ = {"depends": "", "rdepends": "dashed"}
            dictAttr = pair.getAttr()
            if 'style' not in dictAttr:
                # 'depends' dot pairs
                style = ''
            else:
                # currently 'style' only has value 'dashed', means 'rdepends' dot pairs
                style = dictAttr['style']
            filters = [__DictAttr__[case] for case in filters]
            if style not in filters:
                return False
            return True

    def __dotReConstructor(self, pairShow):
        """
        Re-construct dot file based on all dot pairs to show.

        :param set pairShow:        Set of DotPair
        :return str:                Re-constructed content of dot file
        """
        logger.debug("%s.__dotReConstructor: ENTER"%self.__class__)
        content = "digraph G{\n"
        for pair in pairShow:
            content += "    \"%s\" -> \"%s\"" %(pair.getSourceNode(), pair.getDestNode())
            dictAttr = pair.getAttr()
            if dictAttr:
                content += " ["
                for key in dictAttr:
                    content += "%s=\"%s\", " %(key, dictAttr[key])
                content = content[:-2] + "]"
            content += ";\n"
        content += "}\n"
        logger.debug("%s.__dotReConstructor: LEAVE"%self.__class__)
        return content

    def __populateDotFile(self, content, outputFile):
        """
        Populate dot file.

        :param str content:         Re-constructed content of dot file
        :param str outputFile:     Output dot file
        """
        logger.debug("%s.__populateDotFile: ENTER"%self.__class__)
        with open(outputFile, "w") as f:
            f.write(content)
        logger.info("Dot file is populated as: %s"%os.path.realpath(outputFile))
        logger.debug("%s.__populateDotFile: LEAVE"%self.__class__)


if __name__ == "__main__":

    def test_demo():
        my_filter = dot_filter("")
        my_filter.filt("../test/demo.dot", toNode = "printf", fromNode = "main", outputFile = "../test/demo_out.dot")

    def test_systemd():
        my_filter = dot_filter('systemd')
        #my_filter.filt('../test/systemd.dot', toNode = '.*.target', fromNode = '.*.target', filters=['wants', 'after'],
        #               outputFile = '../test/systemd_out.dot')
        my_filter.filt('../test/systemd.dot', toNode = '.*.service', fromNode = 'lazy.target', filters=['wants', 'after'],
                       outputFile = '../test/systemd_out.dot')

    def test_bitbake():
        my_filter = dot_filter('bitbake')
        #my_filter.filt('../test/pn-depends.dot', filters = ['rdepends'], outputFile = '../test/pn-depends_output.dot')
        my_filter.filt('../test/pn-depends.dot', fromNode = '.*conn-connectivity.*app.*', filters = [], outputFile = '../test/pn-depends_output.dot')

    test_bitbake()




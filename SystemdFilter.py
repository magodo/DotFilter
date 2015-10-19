#!/usr/bin/env python
# -*- coding: utf-8 -*-

#########################################################################
# Author: Zhaoting Weng
# Created Time: Sun 18 Oct 2015 06:39:23 PM CST
# File Name: SystemdFilter.py
# Description:
#########################################################################

import argparse
import sys
import lib.dotfilter as dotfilter

parser = argparse.ArgumentParser(prog = "Filter for systemd dot file")
parser.add_argument("input")
parser.add_argument("--from-node", dest="fromNode", default="")
parser.add_argument("--to-node", dest="toNode", default="")
parser.add_argument("--filter", dest="filter", nargs="*", choices=["conflicts", "after", "wants", "requires", "requisite"])
parser.add_argument("--output", "-o", dest="output", default="./output.dot")
Args = parser.parse_args()
sys.exit(dotfilter.filt(Args.input, Args.fromNode, Args.toNode, Args.filter, Args.output))


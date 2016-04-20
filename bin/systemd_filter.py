#!/usr/bin/env python
# -*- coding: utf-8 -*-

#########################################################################
# Author: Zhaoting Weng
# Created Time: Sun 18 Oct 2015 06:39:23 PM CST
# File Name: systemd_filter.py
# Description:
#########################################################################

import argparse
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from lib.dot_filter import dot_filter

parser = argparse.ArgumentParser()
parser.add_argument("input")
parser.add_argument("--from-node", dest="fromNode", default="", help='From which node to extract(regexp supported)')
parser.add_argument("--to-node", dest="toNode", default="",  help='To which node to extract(regexp supported)')
parser.add_argument("--filter", dest="filter", nargs="*", choices=["conflicts", "after", "wants", "requires", "requisite"], help='Which kind of transitions do you want to view')
parser.add_argument("--output", "-o", dest="output", default="./output.dot", help='Output filtered dot file')
Args = parser.parse_args()

dot = dot_filter("systemd")
dot.filt(Args.input, Args.fromNode, Args.toNode, Args.filter, Args.output)


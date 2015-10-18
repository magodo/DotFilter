#!/usr/bin/env python
# -*- coding: utf-8 -*-

#########################################################################
# Author: Zhaoting Weng
# Created Time: Sun 18 Oct 2015 06:39:23 PM CST
# File Name: SystemdViewr.py
# Description:
#########################################################################

import argparse
import sys
import lib.viewer as viewer

parser = argparse.ArgumentParser(prog = "Viewer for systemd dot file")
parser.add_argument("input")
parser.add_argument("--from-node", dest="fromNode", default="")
parser.add_argument("--to-node", dest="toNode", default="")
parser.add_argument("--filter", dest="filter", nargs="*")
parser.add_argument("--output", "-o", dest="output", default="./output.dot")
Args = parser.parse_args()
sys.exit(viewer.view(Args.input, Args.fromNode, Args.toNode, Args.filter, Args.output))


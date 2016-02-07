#!/usr/bin/env python
import sys
import argparse
import os

# Init command line parser
parser = argparse.ArgumentParser()
parser = argparse.ArgumentParser(description='Synapticon Local Documentation Builder')
parser.add_argument('--pull', action="store_true", default=False, help='Pull code for documentation from remote repositories')
parser.add_argument('--build', action="store_true", default=False, help='Build documentation')

# Parse arguments
results = parser.parse_args()

# Make sure at least one argument has been passed to application 
if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)

if (results.pull):
	print 'pulling'
if (results.build):
	os.system('(cd /doc && python sncn-xdoc/xdoc.py html)')
	

sys.exit(0)
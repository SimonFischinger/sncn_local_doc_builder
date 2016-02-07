#!/usr/bin/env python
import sys
import argparse
import os
import re

def main():
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
	
	parse_links()
	
	sys.exit(0)
	

def parse_links():
	directoryList = ['software', 'tutorials', 'tools'];
	ret = {}
	
	for directory in directoryList:
		with open("/doc/" + directory + "/index.rst", "r") as rstFile:
			for rstLine in rstFile:
				#Search for Documentation links in documentation directories
				result = re.search('%s(.*)%s' % ("<", ">"), rstLine)
				if (result != None):
					ret[result.group(1).split('/')[0]] = result.group(1).split('/')[0] 
					
	
				#print rstLine,
	for i in ret:
		print ret[i]
	return ret

def prep_workspace():
	

# Start Main after everything is initialized
if __name__=="__main__":
	main()
   
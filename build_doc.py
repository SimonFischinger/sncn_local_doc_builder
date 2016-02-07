#!/usr/bin/env python
import sys
import argparse
import os
import re
from github import Github
import github
import github.GithubException
import glob
from docutils.nodes import organization

# GLOBAL VARIABLES 
basedir = '/doc/'
directoryList = ['software', 'tutorials', 'tools'];
 
def main():
	# Init command line parser
	parser = argparse.ArgumentParser()
	parser = argparse.ArgumentParser(description='Synapticon Local Documentation Builder')
	parser.add_argument('--download', action="store_true", default=False, help='Download tarballs of repos from github')
	parser.add_argument('--build', action="store_true", default=False, help='Build documentation')

	# Parse arguments
	results = parser.parse_args()

	# Make sure at least one argument has been passed to application 
	if len(sys.argv)==1:
		parser.print_help()
		sys.exit(1)
		
	if (results.download):
		for folder in directoryList:
			download_from_git(parse_links(folder), folder)
	if (results.build):
		prep_workspace()
		#os.system('(cd /doc && python sncn-xdoc/xdoc.py html)')
	
	
	
	sys.exit(0)
	

def parse_links(directory):
	ret = {}

	with open(basedir + directory + "/index.rst", "r") as rstFile:
		for rstLine in rstFile:
			#Search for Documentation links in documentation directories
			result = re.search('%s(.*)%s' % ("<", ">"), rstLine)
			if (result != None):
				ret[result.group(1).split('/')[0]] = result.group(1).split('/')[0] 
	return ret

def prep_workspace():
	''' 
	1. Check if sncn_xdoc is checked out - otherwise pull from git
	2. Check for Symlinks and offer to replace those directories by gitpull
	'''
	# Check if sncn-xdoc is available in doc directory
	if not os.path.isdir(basedir + "/sncn-xdoc"):
		print "Didn't find sncn-xdoc -> download"
		download_from_git({'sncn-xdoc'}, '.')
	
	
	# Check if workspace contains links
	for d in directoryList:
		dirname = glob.glob(basedir + d + "/*")			
		firstHit = True		
		for name in dirname:
			if os.path.islink(name):
				if firstHit:
					firstHit = False
					print "\n\n!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
					print "! Symlinks to repositories found, symlinks are not supported by this version of the document generator.  !" 
					print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
					inp = raw_input ("Do you want to replace links with data from Github? [y/n] ")
					if inp is 'n':
						print "Stopping documentation builder. Cannot build based on Symbolic Links... "
						exit()
						
				print name + " is link!\n"
				print "Delete Link..."
				#os.remove(name)
	# Symbolic link has been found and removed -> Check Github for data
	if firstHit:
		print "Checking Github for documentation data ... "
		for d in directoryList:
			download_from_git(parse_links(d), d)
		
	
def download_from_git(repositories, directory):
	g = Github("SimonFischinger", "669c2d295a52eccbbbd9a12480941140105f83a5")
	sncn_orgs = ("synapticon", "sncn-private", "sncn-hub")
	
	for org in g.get_user().get_orgs():
		if (org.login in sncn_orgs):
			for repo in org.get_repos():
				if (repo.name in repositories):
					link = repo.get_archive_link("tarball", "develop")
					
					# Check if folder already exists -> if so, skip
					if os.path.isdir(basedir + directory + "/" + repo.name):
						print repo.name + " already exists - skip"
						continue
					
					print "\n\nDownloading repo " + repo.name + "...."
					
					# Download repository as tarball from github and extract it
					os.system("(cd " + basedir + directory + " && wget " + link + " -O" + repo.name + ".tar.gz)")
					
					# Unpack
					print "Extract downloaded files... \n"
					os.system("(cd " + basedir + directory + " && tar -zxvf " + repo.name + ".tar.gz)")
					
					# Remove tarball
					print "\nRemove tarball..."
					os.remove(basedir + directory + "/" + repo.name + ".tar.gz")
					
					# Search for extracted directory including hash and rename to original name
					print "Rename to final name..."
					dirname = glob.glob(basedir + directory + "/*" + repo.name + "*")
					
					# Change name of unpacked repository data to correct name				
					if dirname:
						os.rename(glob.glob(basedir + directory + "/*" + repo.name + "*").pop(), basedir + directory + "/" + repo.name)
	
		
	return

# Start Main after everything is initialized
if __name__=="__main__":
	main()
   
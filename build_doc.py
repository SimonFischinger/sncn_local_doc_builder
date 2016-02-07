#!/usr/bin/env python
import sys
import argparse
import os
import re
from github import Github
import github
import github.GithubException

import wget
from docutils.nodes import organization

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
		download_from_git(parse_links('software'), 'software')
	if (results.build):
		os.system('(cd /doc && python sncn-xdoc/xdoc.py html)')
	
	
	
	sys.exit(0)
	

def parse_links(directory):
	#directoryList = ['software', 'tutorials', 'tools'];
	ret = {}

	with open("/doc/" + directory + "/index.rst", "r") as rstFile:
		for rstLine in rstFile:
			#Search for Documentation links in documentation directories
			result = re.search('%s(.*)%s' % ("<", ">"), rstLine)
			if (result != None):
				ret[result.group(1).split('/')[0]] = result.group(1).split('/')[0] 
				

				#print rstLine,
	#for i in ret:
	#	print ret[i]
	return ret

def prep_workspace():
	''' 
	1. Check for Symlinks and offer to replace those directories by gitpull
	2. Check for (other) missing directories based on result of parse_links()
	3. Try to download all missing files from git (search synapticon standard repos)
	4. Check if sncn_xdoc is checked out - otherwise pull from git
	'''
	
def download_from_git(repositories, directory):
	g = Github("SimonFischinger", "7ecff6faa079fc22e1be0cd3c4dc46cf2de4b772")
	sncn_orgs = ("synapticon", "sncn-private", "sncn-hub")
	for org in g.get_user().get_orgs():
#		print org.login
#		continue
		if (org.login in sncn_orgs):
			for repo in org.get_repos():
				if (repo.name in repositories):
					link = repo.get_archive_link("tarball", "develop")
					print link + "\n"
					print repo.name + "\n"
					os.system("(cd test && wget " + link + " -O" + repo.name + ".tar.gz)")
					#wget.download(link, 'test/' + repo.name + '.tar.gz')
		
	return

# Start Main after everything is initialized
if __name__=="__main__":
	main()
   
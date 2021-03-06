#!/usr/bin/python
#
# wtcommit.py
#
# A script to use ngerakines' What The Commit (https://github.com/ngerakines/commitment)
# messages into your own commits.
#
# Developed by Bruno Jurkovski

import sys
import urllib2
import commands
from HTMLParser import HTMLParser

class WTCommitParser(HTMLParser):
	def __init__(self):
		self.readingContent = False
		self.readFirstP = False
		self.readTag = False
		self.commitMsg = ""
		HTMLParser.__init__(self)

	def handle_starttag(self, tag, attrs):
		try:
			if tag == "div":
				for attr in attrs:
					if attr[0] == "id" and attr[1] == "content":
						self.readingContent = True
			elif tag == "p" and self.readingContent and not self.readFirstP:
				self.readTag = True
		except:
			pass

	def handle_data(self, data):
		if self.readTag:
			self.commitMsg = data
			self.readTag = False

	def handle_endtag(self, tag):
		if (tag == "div") and self.readingContent:
			self.readingContent = False
		elif tag == "p" and self.readingContent and not self.readFirstP:
			self.readFirstP = True

if __name__ == "__main__":
	# Fetches the page
	url = "http://whatthecommit.com/"
	req = urllib2.Request(url)
	response = urllib2.urlopen(req)
	page = response.read()

	# Parse its HTML to get the commit message
	parser = WTCommitParser()
	parser.feed(page)

	# Chop the \n in the end of the message
	msg = parser.commitMsg
	if msg[len(msg)-1] == '\n':
		msg = msg[0:len(msg)-1]

	# Instructions in case of bad usage
	if len(sys.argv) < 2:
		print "Usage:", sys.argv[0], "[git/svn]"
		exit()

	# Parse parameters given by the user
	extraMsg = ""
	for i in range(2, len(sys.argv)):
		if sys.argv[i] == "-m" and i+1<len(sys.argv):
			extraMsg = " (" + sys.argv[i+1] + ")"
			break

	# Make the real commit
	if sys.argv[1] == "svn":
		print commands.getoutput("svn commit -m '" + msg + extraMsg + "'")
	elif sys.argv[1] == "git":
		print commands.getoutput("git commit . " + "-m '" + msg + extraMsg + "'")
	else:
		print "First parameter must be either 'git' or 'svn'."
		exit()

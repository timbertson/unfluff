#!/usr/bin/env python

import sys

import misc
from extraction import Extraction

# convenience functions
def from_url(u):
	import urllib2
	return _from_open_stream(urllib2.urlopen(u))

def from_file(u):
	if u == '-':
		return from_string(sys.stdin.read())
	return _from_open_stream(open(u))

def _from_open_stream(f):
	try:
		return Extraction(f.read())
	finally: f.close()

def from_string(s):
	return Extraction(s)

def main():
	from optparse import OptionParser
	parser = OptionParser("%prog [options] file")
	parser.add_option('-u', '--url', help='load url (instead of file)')
	parser.add_option('-v', '--verbose', action='store_true', help='verbose messaging')
	opts, args = parser.parse_args()
	if opts.verbose:
		misc.set_debug(True)
	if not (opts.url or len(args) == 1):
		parser.print_help()
		return 1
	if opts.url:
		doc = from_url(opts.url)
	else:
		doc = from_file(args[0])
	print doc


if __name__ == '__main__':
	sys.exit(main())


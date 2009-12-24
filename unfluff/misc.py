import sys

DEBUG = False

def debug(s):
	if not DEBUG: return
	print >> sys.stderr, s

def set_debug(val):
	global DEBUG
	DEBUG = val

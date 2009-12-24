#!/usr/bin/env python

# adapted from http://www.spicylogic.com/allenday/blog/2008/05/27/statistical-html-content-extraction/

import sys
from lxml import etree
from scipy.special import gammaln
from math import exp

DEBUG = False

def debug(s):
	if not DEBUG: return
	print >> sys.stderr, s

def hypergeometric(*a):
	## this should work:
	#from scipy import stats
	#return stats.hypergeom.pmf(*a)

	## but it doesn't. this is a reasonable workaround, from http://bytes.com/topic/python/answers/439096-hypergeometric-distribution
	return hypergeometric_gamma(*a)

def lnchoose(n, m):
	nf = gammaln(n + 1)
	mf = gammaln(m + 1)
	nmmnf = gammaln(n - m + 1)
	return nf - (mf + nmmnf)

def hypergeometric_gamma(k, n1, n2, t):
	if t > n1 + n2:
		t = n1 + n2
	if k > n1 or k > t:
		return 0
	elif t > n2 and ((k + n2) < t):
		return 0
	else:
		c1 = lnchoose(n1,k)
		c2 = lnchoose(n2, t - k)
		c3 = lnchoose(n1 + n2 ,t)
	return exp(c1 + c2 - c3)


class Extraction(object):
	IGNORE = set(['head', 'iframe', 'script', 'style'])
	ELEMENT_WEIGHTS = {
		# we like these
		'h1': -1,
		'h2': -1,
		'blockquote': -1,
		'pre': -1,
		# don't penalize these "content" tags
		'a': 0,
		'b': 0,
		'br': 0,
		'div': 0,
		'em': 0,
		'h3': 0,
		'h4': 0,
		'i':0,
		'p':0,
		'span':0,
		'strong':0,
		# discourage things that are often found in fluff:
		'li': 3,
		'form':1,
	}
	DEFAULT_WEIGHT = 2
	REMOVE_ATTRS = set(['style'])

	def __init__(self, html_string):
		self.minp = 1
		self.root = self.parse(html_string)
		self.elemtotal, self.wordtotal = self.tally(self.root)
		self.examine(self.root)
	
	def __str__(self):
		debug("CONTENT: %s" % (self._str(self.content)))
		return etree.tostring(self.content, pretty_print=True)
		
	def parse(self, file):
		parser = etree.HTMLParser(remove_blank_text=True, remove_comments=True)
		return etree.HTML(file, parser)
	 
	def examine(self, node):
		elemcount, wordcount = self.tally(node);

		total_entities = self.elemtotal + self.wordtotal
		node_entities = wordcount + elemcount
		p = hypergeometric( wordcount, self.elemtotal + self.wordtotal, self.wordtotal, elemcount + wordcount )
		debug(repr(( wordcount, self.elemtotal + self.wordtotal, self.wordtotal, elemcount + wordcount )))
		debug("p for %s = %s" % (self._str(node), p))
	 
		if p < self.minp and node.tag not in self.IGNORE:
			text = self.cleanup(node)
			self.minp = p
			self.content = text

		for child in list(node):
			self.examine(child)
	
	def tally(self, node, elemcount = 0, wordcount = 0):
		"""return elemcount, wordcount for a given node and its (recursive) subtree"""
		if node.tag not in self.IGNORE:
			words = (node.text or '').split()
			if len(words) > 1:
				wordcount += len(words)

		for child in list(node):
			elemcount += self.ELEMENT_WEIGHTS.get(child.tag, self.DEFAULT_WEIGHT)
			if child.tag not in self.IGNORE:
				elemcount, wordcount = self.tally(child, elemcount, wordcount)
		
		debug("element %s has %s nodes and %s words" % (self._str(node), elemcount, wordcount))
		return max(elemcount,0), wordcount
		
	
	def _str(self, elem):
		return "%s(%s: %r)" % (elem, elem.tag, elem.attrib)

	def cleanup(self, root):
		for node in root.getiterator():
			[node.remove(child) for child in node if child.tag in self.IGNORE]
			for attr in self.REMOVE_ATTRS:
				if attr in node.attrib:
					del node.attrib[attr]
		return root


# convenience functions
def url(u):
	import urllib2
	f = urllib2.urlopen(u)
	try:
		return Extraction(f.read())
	finally: f.close()

def file(u):
	if u == '-':
		return Extraction(sys.stdin.read())
	f = open(u)
	try:
		return Extraction(f.read())
	finally: f.close()

def main(argv):
	global DEBUG
	from optparse import OptionParser
	parser = OptionParser("%prog [options] file")
	parser.add_option('-u', '--url', help='load url (instead of file)')
	parser.add_option('-v', '--verbose', action='store_true', help='verbose messaging')
	opts, args = parser.parse_args(argv)
	if opts.verbose:
		DEBUG = True
	if opts.url or len(args) == 1:
		if opts.url:
			doc = url(opts.url)
		else:
			doc = file(args[0])
		print doc
	else:
		parser.print_help()
		return 1


if __name__ == '__main__':
	sys.exit(main(sys.argv[1:]))


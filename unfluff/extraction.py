# adapted from http://www.spicylogic.com/allenday/blog/2008/05/27/statistical-html-content-extraction/

from lxml import etree
from math import log
import re

from probability import hypergeometric
from misc import debug

class Extraction(object):
	IGNORE = set(['head', 'iframe', 'script', 'style'])
	ELEMENT_WEIGHTS = {
		# we like these
		'h1': -0.5,
		'h2': -0.5,
		'blockquote': -0.5,
		'pre': -1,
		'a': 0.8,
		'b': 0,
		'br': 0.1,
		'div': 0.5,
		'em': 0,
		'h3': 0,
		'h4': 0,
		'i':0,
		'p':0.1,
		'span':0.5,
		'strong':0,
		# discourage things that are often found in fluff:
		'li': 2,
		'form':3,
	}
	DEFAULT_WEIGHT = 1
	REMOVE_ATTRS = set(['style'])
	BLACKLIST_ATTRS = {
		'class': re.compile(r'\bcomment', re.I),
		'id': re.compile(r'\bcomment', re.I),
	}
	GOOD_CLASSES = set([re.compile('\bpost\b', re.I), re.compile('\bcontent\b', re.I)])
	MAX_PURITY = 80

	def __init__(self, html_string):
		self.maxp = 0
		self.stats = []
		self.root = self.parse(html_string)
		self.cleanup(self.root)
		self.content = self.root
		self.elemtotal, self.wordtotal, self.depthtotal = self.tally(self.root)
		self.examine(self.root)
	
	def __str__(self):
		debug("CONTENT: %s" % (self._str(self.content)))
		return etree.tostring(self.content, pretty_print=True)
		
	def parse(self, file):
		parser = etree.HTMLParser(remove_blank_text=True, remove_comments=True)
		return etree.HTML(file, parser)
	 
	def examine(self, node):
		elemcount, wordcount, depth = self.tally(node);
		#if elemcount == 0 or wordcount == 0:
		#	return

		# 0-1 with 0 being the whole document and 1 being a single node
		shallowness = (1 - (float(depth) / self.depthtotal))

		# 0-1 with 0 being no volume, 1 being entire volume (capped at 1000 words)
		volume_proportion = min(float(min(wordcount, 1000)) / self.wordtotal, 1)
		volume_proportion = log((8*volume_proportion) + 1, 2) / 3

		purity = float(wordcount) / max(elemcount, 1)
		# what is max_purity? I guess anything above 20:1 is a bit mad...
		purity = min((float(purity) / self.MAX_PURITY), 1)


		# now scale 'em for importance:
		#volume_proportion = ((volume_proportion - 1) * 0.25) + 1
		volume_proportion *= 5
		purity *= 2
		shallowness *= 1

		p = shallowness + volume_proportion + purity

		if node.tag not in self.IGNORE:
			if elemcount > 0 and p > (0.5 * self.maxp):
				self.stats.append({
					'node': node,
					'volume': volume_proportion,
					'elems': elemcount,
					'shallowness': shallowness,
					'purity': purity,
					'p': p
				})
			if p > self.maxp:
				self.maxp = p
				self.content = node

		for child in list(node):
			self.examine(child)
	
	def tally(self, node, elemcount = 0, wordcount = 0):
		"""return elemcount, wordcount for a given node and its (recursive) subtree"""
		if node.tag not in self.IGNORE:
			words = (node.text or '').split()
			if len(words) > 1:
				wordcount += len(words)

		cls = node.attrib.get('class', None)
		if cls:
			if any((matcher.search(cls) for matcher in self.GOOD_CLASSES)):
				worcount *= 1.5
		tagdepth = 0
		for child in list(node):
			elemcount += self.ELEMENT_WEIGHTS.get(child.tag, self.DEFAULT_WEIGHT)
			if child.tag not in self.IGNORE:
				elemcount, wordcount, child_tagdepth = self.tally(child, elemcount, wordcount)
				tagdepth = max(tagdepth, child_tagdepth + 1)
		
		debug("element %s has %s nodes, %s depth and %s words" % (self._str(node), elemcount, tagdepth, wordcount))
		return max(elemcount,0), wordcount, tagdepth
		
	
	def _str(self, elem):
		return "%s(%s: %r)" % (elem, elem.tag, elem.attrib)

	def cleanup(self, root):
		for node in root.getiterator():
			for attr in self.REMOVE_ATTRS:
				if attr in node.attrib:
					del node.attrib[attr]
			for attr, val in self.BLACKLIST_ATTRS.items():
				if attr in node.attrib and val.search(node.attrib[attr]):
					del node
					break
		return root

import sys

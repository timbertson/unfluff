import pyx
import readline
import sys
import math

def graph(stats, debug=0):
	g = pyx.graph.graphxy(width=34, height=6, x=pyx.graph.axis.bar())
	lines = []
	for stat in stats:
		line = (stat['volume'], stat['volume'] + stat['purity'], stat['volume'] + stat['purity'] + stat['shallowness'])
		lines.append(line)
		#print repr(line)
		#break
	data = pyx.graph.data.list(lines, xname=0, y=1, b=2, c=3)
	g.plot(data,
		[
			pyx.graph.style.bar([pyx.color.rgb.green]),
			pyx.graph.style.stackedbarpos("b"),
			pyx.graph.style.bar([pyx.color.rgb.blue]),
			pyx.graph.style.stackedbarpos("c"),
			pyx.graph.style.bar([pyx.color.rgb.red]),
		])
	g.writePDFfile("stacked")

	def line(*parts, **kw):
		line = []
		i=0
		for st in stats:
			st_elems = [st[key] for key in parts]
			mod = kw.get('mod', lambda x: x)
			line.append((i, mod(*st_elems)))
			i += 1
		return line

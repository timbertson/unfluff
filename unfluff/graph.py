import Gnuplot
import readline
import sys
import math

def graph(stats, debug=0):
	g = Gnuplot.Gnuplot(debug=debug)
	g.title('node breakdown') # (optional)
	g('set data style linespoints') # give gnuplot an arbitrary command

	def line(*parts, **kw):
		line = []
		i=0
		for st in stats:
			st_elems = [st[key] for key in parts]
			mod = kw.get('mod', lambda x: x)
			line.append((i, mod(*st_elems)))
			i += 1
		return line

	def power_ratio(p, scale=1.0):
		return lambda words, elems: (scale * pow(words, p)) / (elems or 1)

	while True:
		try:
			print >> sys.stderr, "\nenter formula (using <words, elems>):"
			input = raw_input()
		except EOFError: break
		try:
			#factor, scale = map(float, input.split())
			g.plot(
				line('words'),
				#line('words', 'elems', mod=power_ratio(factor, scale=scale))
				line('words', 'elems', mod=eval("lambda words, elems: %s" % input))
			)
		except Exception, e:
			print e
			pass

import time
def graph_awesomeness_graphs(func):
	for plot_info in [getattr(func, x) for x in ('expected_volume_ratio', 'volume_accuracy_confidence', 'purity_importance')]:
		plot = Gnuplot.Gnuplot(debug=1)
		plot.set_range('xrange', plot_info['xrange'])
		plot.set_range('yrange', plot_info['yrange'])
		plot.title(plot_info['label'])
		plot.plot(plot_info['formula'])
		time.sleep(2 * 1000)

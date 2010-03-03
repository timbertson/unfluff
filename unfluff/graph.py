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
	#g.plot(
	#	line('words', mod=lambda x: 0.1 * x),
	#	#line('words_per_tag'),
	#	line('words', 'elems', mod=power_ratio(2, scale=0.5)),
	#	#line('words', 'elems', mod=power_ratio(1.4, scale=0.7)),
	#	#line('words', 'elems', mod=power_ratio(1.5, scale=0.5)),
	#	#pick(stats, 'words_per_tag'),
	#	#multiply_y(0.02, pick(stats, 'words')),
	#	#multiply_y(60, pick(stats, 'p'))
	#)
	#g.hardcopy(filename="graph.ps")
	#raw_input('\n')

def graph_awesomeness_graphs(awesomeness_func):
	for plot_info in [func[x] for x in ('expected_volume_ratio', 'purity_importance']:
		plot = Gnuplot.Gnuplot(debug=1)
		plot.set_range('xrange', plot_info['xrange'])
		plot.set_range('yrange', plot_info['yrange'])
		plot.title(plot_info['label'])
		plot.plot(plot_info['formula'])
	
	raw_input('press enter to continue)

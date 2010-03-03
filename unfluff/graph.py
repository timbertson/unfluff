import Gnuplot

def pick(data, idx):
	ret = []
	i = 0
	for d in data:
		ret.append((i, d[idx]))
		i+=1
	return ret

def multiply_y(factor, data):
	def mult(d):
		x,y = d
		return (x, y * factor)
	return map(mult, data)

def graph(stats):
	g = Gnuplot.Gnuplot(debug=1)
	g.title('node breakdown') # (optional)
	g('set data style linespoints') # give gnuplot an arbitrary command
	g.plot(
		pick(stats, 'words_per_tag'),
		multiply_y(0.5, 'words'),
		multiply_y(60, pick(stats, 'p')))
	g.hardcopy(filename="graph.ps")
	raw_input('Please press return to continue...\n')

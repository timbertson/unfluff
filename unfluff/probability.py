from scipy.special import gammaln
from scipy.stats import norm
from math import exp

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


def awesomeness_func(volume_expectation_sharpness, base_volume_expectancy_shift, purity_importance_scale, volume_accuracy_confidence, base_purity_importance):
	"""
	volume_expectation_sharpness:  how quickly volume expectency climbs to 1.0 as document volume rises
	base_volume_expectancy_shift:  minimum volume expectency (shift on x axis)
	purity_importance_scale:       scaling factor of how important purity is
	volume_accuracy_confidence:    how harshly we should judge nodes for diverging from the expected volume
	base_purity_importance:        purity importance offset
	"""
	def volume(words, tags):
		return words + tags

	def func(words, tags, root_words, root_tags):
		tag_volume = volume(words, tags)
		root_volume = volume(root_words, root_tags)
		expected_volume_ratio = (volume_expectation_sharpness * (-1.0 / (x + base_volume_expectancy_shift))) + 1
		expected_volume = expected_volume_ratio * root_volume
		purity_importance = (purity_importance_scale * norm.cdf((float(expected_volume - tag_volume) / root_volume) * volume_accuracy_confidence)) + base_purity_importance
		p = (tag_volume) / (purity * purity_importance)

		result = dict(
			p=p,
			root_volume=root_volume,
			purity_importance=purity_importance,
			expected_volume=expected_volume,
			tag_volume=tag_volume
		}
		return result
	
	# x is between zero (the correct volume) and one (expected=0, actual=100% of document (or vice versa))
	func.purity_importance = {
		'formula': "(%(purity_importance_scale)s * norm.cdf(x) * %(volume_accuracy_confidence)s)) + %(base_purity_importance)s" % dict(
			purity_importance_scale=purity_importance_scale,
			volume_accuracy_confidence=volume_accuracy_confidence,
			base_purity_importance=base_purity_importance),
		'xrange': (0, 1),
		'yrange': (0, 1),
	}

	func.expected_volume_ratio = {
		'formula':"(%(volume_expectation_sharpness) * (-1.0 / (x + %(base_volume_expectancy_shift)))) + 1" % dict(
			volume_expectation_sharpness = volume_expectation_sharpness,
			base_volume_expectancy_shift = base_volume_expectancy_shift),
		'xrange': (0, 1000),
		'yrange': (0, 1),
		'label': "expected volume ratio (for documents of x words and tags)",
	}

	return func

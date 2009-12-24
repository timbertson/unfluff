from scipy.special import gammaln
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


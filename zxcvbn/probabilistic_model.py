import os

class ProbabilisticModel:
	def __init__(self, filename, n=10**5, count=False):
		self.count = count
		self.dumpfile = "%s.%s.dump" % (filename, self.__class__.__name__)
		self.n = n
		if os.path.isfile(self.dumpfile):
			self.load(self.dumpfile)
		else:
			print("Learning")
			self.learn(filename)
			print("Sampling")
			self.sample = self.monte_carlo_sample(n)
			self.dump(self.dumpfile)

	def dump(self, filename):
		raise NotImplementedError

	def load(self, filename):
		raise NotImplementedError

	def learn(self, filename):
		raise NotImplementedError

	def proba(self, word):
		raise NotImplementedError

	def monte_carlo_sample(self, n):
		raise NotImplementedError

	def get_rank(self, word):
		n = len(self.sample)
		if len(word) >= 40:
			return 1e20
		p = self.proba(word)
		if not p:
			return 1e20
		rank = sum([1/(s*n) for s in self.sample if s > p])
		return rank
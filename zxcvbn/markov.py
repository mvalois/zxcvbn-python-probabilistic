import os
from .probabilistic_model import ProbabilisticModel

from ngram import NGram as ngram

from collections import defaultdict as ddict
from types import SimpleNamespace

class Markov(ProbabilisticModel):
	def __init__(self, filename, n=10**5, count=False, N=3, nblevel=10):
		self.probas = ddict(ddict(float))
		self.nb_ngrams = ddict(int)
		self.N = N
		self._ngrams_obj = ngram(N=self.N)
		super().__init__(filename, n, count)

	def dump(self, filename):
		pickle.dump((self.probas, self.nb_grams, self.N), open(filename, 'wb'))

	def load(self, filename):
		self.probas, self.nb_grams, self.N = pickle.load(open(filename, 'rb'))

	def learn(self, filename):
		with open(filename) as inbuff:
			for word in inbuff:
				word = word.rstrip()
				if self.count:
					word, count = word.split(maxsplit=1)
					count = int(count)
				else:
					count = 1
				self.parse(word, count)
		for lhs, rhs in self.probas:
			k = sum(rhs.values())
			for g in rhs:
				rhs[g] /= k

	def proba(self, word):
		p = 1
		gramms = [g for g in self._ngrams_obj.ngrams(word)]
		if gramms[0] not in self.probas[chr(0)]:
			return 0
		p *= self.probas[chr(0)][gramms[0]]
		if gramms[-1] not in self.probas[chr(1)]:
			return 0
		p *= self.probas[chr(1)][gramms[-1]]
		for i, g in zip(range(1+len(gramms)), gramms[1:-1]):
			if g not in self.probas[gramms[i-1]]:
				return 0
			p *= self.probas[gramms[i-1][1:]]
		return p

	def monte_carlo_sample(self, n):
		pass

	def parse(self, word, count):
		"""
		Compute all n-grams of word
		and store number of occurrences
		"""
		gramms = [g for g in self._ngrams_obj.ngrams(word)]
		self.probas[chr(0)][gramms[0]] += count
		self.probas[gramms[-1]][chr(1)] += count
		for i, g in zip(range(1+len(gramms)), gramms[1:-1]):
			self.probas[gramms[i-1][1:]] += count
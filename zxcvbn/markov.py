import os
import pickle
import random
from .probabilistic_model import ProbabilisticModel

from ngram import NGram as ngram

from collections import defaultdict as ddict

S = chr(0)
E = chr(1)

def get_ddict():
	return ddict(float)

class Markov(ProbabilisticModel):
	def __init__(self, filename, n=10**5, count=False, N=3, nblevel=10):
		self.probas = ddict(get_ddict)
		self.N = N
		self._ngrams_obj = ngram(N=self.N)
		super().__init__(filename, n, count)

	def dump(self, filename):
		pickle.dump((self.probas, self.N, self.sample), open(filename, 'wb'))

	def load(self, filename):
		self.probas, self.N, self.sample = pickle.load(open(filename, 'rb'))

	def learn(self, filename):
		with open(filename) as inbuff:
			for word in inbuff:
				word = word.strip()
				if self.count:
					count, word = word.split(maxsplit=1)
					count = int(count)
				else:
					count = 1
				if len(word) >= self.N:
					self.parse(word, count)
		for lhs, rhs in self.probas.items():
			k = sum(rhs.values())
			for g in rhs:
				rhs[g] /= k

	def proba(self, word):
		p = 1
		gramms = [g for g in self._ngrams_obj.ngrams(word)]
		p *= self.probas[S][gramms[0][:-1]]
		p *= self.probas[gramms[-1][1:]][E]
		for g in gramms:
			p *= self.probas[g[:-1]][g]
		return p

	def odict(self, d):
		pop = ([],[])
		for k, v in d.items():
			pop[0].append(k)
			pop[1].append(v)
		return pop

	def monte_carlo_sample(self, n):
		psamples = list()
		for i in range(n):
			pop = self.odict(self.probas[S])
			g = random.choices(pop[0], pop[1], k=1)[0]
			p = self.probas[S][g]
			while True:
				pop = self.odict(self.probas[g])
				ng = random.choices(pop[0], pop[1], k=1)[0]
				p *= self.probas[g][ng]
				if ng == E:
					break
				g = ng[1:]
			psamples.append(p)
		return psamples

	def parse(self, word, count):
		"""
		Compute all n-grams of word
		and store number of occurrences
		"""
		gramms = [g for g in self._ngrams_obj.ngrams(word)]
		self.probas[S][gramms[0][:-1]] += count
		self.probas[gramms[-1][1:]][E] += count
		for g in gramms:
			self.probas[g[:-1]][g] += count
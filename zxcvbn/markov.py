import os
import pickle
import random
from .probabilistic_model import ProbabilisticModel
from . import ngram_parse
from _ngram_parse import ffi, lib as plib

from collections import defaultdict as ddict

S = chr(0)
E = chr(1)

def get_ddict():
	return ddict(float)

class Markov(ProbabilisticModel):
	def __init__(self, filename, n=10**5, count=False, N=3, nblevel=10):
		self.probas = ddict(get_ddict)
		self.N = N
		super().__init__(filename, n, count)

	def dump(self, filename):
		pickle.dump((self.probas, self.N, self.sample), open(filename, 'wb'))

	def load(self, filename):
		self.probas, self.N, self.sample = pickle.load(open(filename, 'rb'))

	def learn(self, filename):
		with open(filename) as inbuff:
			for word in inbuff:
				word = word.strip()
				if len(word) > 40:
					continue
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
		if len(word) > 40 or len(word) < self.N:
			return 0
		p = 1
		gramms = plib.parse(ffi.new("wchar_t[]", word), self.N)
		gramms = [ffi.string(gramms.grams[i]) for i in range(gramms.nbngrams)]
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
		gramms = plib.parse(ffi.new("wchar_t[]", word), self.N)
		gramms = [ffi.string(gramms.grams[i]) for i in range(gramms.nbngrams)]
		self.probas[S][gramms[0][:-1]] += count
		self.probas[gramms[-1][1:]][E] += count
		for g in gramms:
			self.probas[g[:-1]][g] += count
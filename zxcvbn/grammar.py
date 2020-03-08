import os
import string
import random
import pickle
import multiprocessing as mp
from collections import defaultdict as ddict
from . import grammar_parse
from _parse import ffi, lib as plib

def S(): return 'S'

class Grammar:
	def __init__(self, filename, n=10**5, count=False):
		# If letter is not lower or digit it's special
		self.type = ddict(S)
		for alpha in string.ascii_letters:
			self.type[alpha] = 'L'
		for digit in string.digits:
			self.type[digit] = 'D'
		""" e.g.
		{"L6_D2": 0.1,
		 "L4_D2": 0.9,
		}
		"""
		self.base = ddict(float)
		""" e.g.
		{"D1": {"0": 0.1,
				"1": 0.9},
		 "S4": {"!!!!": 0.2,
				"$$$$": 0.8}
		}
		"""
		self.terminals = ddict(dict)
		self.ordered_terms = dict()
		self.count = count
		grammar_dump = 'grammar.mcs'
		if os.path.isfile(grammar_dump):
			self.sample = pickle.load(open(grammar_dump, 'rb'))
		else:
			print("Learning")
			self.learn(filename)
			print("Sampling")
			self.sample = self.monte_carlo_sample(n)
			pickle.dump(self.sample, open(grammar_dump, 'wb'))


	def learn(self, filename):
		"""
		Iterate over filename,
		parse each word,
		and normalize probas
		between [0,1]
		"""
		with open(filename) as _buffer:
			for line in _buffer:
				if self.count:
					count, *word = line.split()
					count = int(count)
					word = ' '.join(word)
				else:
					word = line.rstrip()
				self.cparse(word)
		nb_bases = sum(self.base.values())
		for _str, proba in self.base.items():
			self.base[_str] = proba / nb_bases

		for _str, term_proba in self.terminals.items():
			nb_terms = sum([proba for proba in term_proba.values()])
			for term, proba in term_proba.items():
				term_proba[term] = proba / nb_terms

	def cparse(self, word, occ=1):
		if len(word) == 0 or len(word) >= 20:
			return
		try:
			gramm = plib.parse(word.encode('ascii'))
		except UnicodeEncodeError:
			return
		base = ffi.string(gramm.base).decode()
		nbterms = gramm.nbterms
		comp_base = list()
		for i in range(nbterms):
			term = ffi.string(gramm.terms[i]).decode()
			term_len = len(term)
			sous_base = base[0] + str(term_len)
			if term in self.terminals[sous_base]:
				self.terminals[sous_base][term] += occ
			else:
				self.terminals[sous_base][term]  = occ
			comp_base.append(sous_base)
			base = base[term_len:]
		base = '_'.join(comp_base)
		self.base[base] += occ

	def proba(self, word):
		gramm = plib.parse(word.encode('ascii'))
		base = ffi.string(gramm.base).decode()
		nbterms = gramm.nbterms
		proba = 1
		comp_base = ""
		for i in range(nbterms):
			term = ffi.string(gramm.terms[i]).decode()
			term_len = len(term)
			sous_base = base[0] + str(term_len)
			comp_base += sous_base
			if term not in self.terminals[sous_base]:
				return 0
			proba *= self.terminals[sous_base][term]
		if comp_base not in self.base:
			return 0
		proba *= self.base[comp_base]
		return proba

	def sousbase_sample(self, arg):
		base, p = arg
		for sous_base in base.split('_'):
			if sous_base not in self.cache:
				psous_bases = list()
				for term, pterm in self.terminals[sous_base].items():
					psous_bases.append(pterm)
				self.cache[sous_base] = psous_bases
			else:
				psous_bases = self.cache[sous_base]
			p *= random.choices(psous_bases, psous_bases)[0]
		return p

	def monte_carlo_sample(self, n):
		bases = list()
		pbases = list()
		for base, p in self.base.items():
			bases.append((base,p))
			pbases.append(p)
		bases_samples = random.choices(bases, pbases, k=n)
		psamples = list()
		self.cache = dict()
		pool = mp.Pool()
		for p in pool.imap_unordered(self.sousbase_sample, bases_samples, chunksize=n//pool._processes):
			psamples.append(p)
		return sorted(psamples, reverse=True)

	def get_rank(self, word):
		n = len(self.sample)
		p = self.proba(word)
		rank = sum([1/(s*n) for s in self.sample if s > p])
		return rank
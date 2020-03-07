from time import time
import pickle

# import matplotlib.pyplot as plt

from . import grammars as gr
from . import grammar_utils as gru
from . import random_set as rdset



def construct_dict(d):
    f = open(d, "r")
    d = dict()
    for l in f:
        n = int(l[:8])
        w = l[8:]
        d[w] = n
    return d


def construct_time_test(dico, name, n):
    d_length = len(dico)//(pow(2, 10))

    lengths = []
    times = []

    for j in range(1, n+1):
        if j < n:
            _ranked_dictionaries = {name: dict()}

            count = 0
            for e in dico:
                if count >= pow(2, j)*d_length:
                    break;
                count += 1
                _ranked_dictionaries[name][e] = dico[e]
        else:
            _ranked_dictionaries = {name: dico}
        composed_bases_dict = dict()
        simple_bases_dict = dict()

        cb_counter = 0
        sb_counter = 0

        tmp_cb_dict = dict()
        tmp_sb_lists = dict()

        t1 = time()

        for dictionary_name, frequency_dict in _ranked_dictionaries.items():
            iter_verif = 0
            ll = len(frequency_dict) // 100
            for w in frequency_dict:

                if w != "":
                    if iter_verif % ll == 0: print(iter_verif // ll, '%')
                    iter_verif += 1

                    k = frequency_dict[w]
                    simple_bases, composed_base = gru.bases(w)

                    if composed_base in tmp_cb_dict:
                        tmp_cb_dict[composed_base] += k
                    else:
                        tmp_cb_dict[composed_base] = k
                    simple_bases_pattern = gru.cut(composed_base)

                    for i in range(len(simple_bases)):
                        p = simple_bases_pattern[i]

                        if p in tmp_sb_lists:
                            if simple_bases[i] in tmp_sb_lists[p]:
                                tmp_sb_lists[p][simple_bases[i]] += k
                            else:
                                tmp_sb_lists[p][simple_bases[i]] = k
                        else:
                            tmp_sb_lists[p] = {simple_bases[i]: k}

                    cb_counter += k
                    if composed_base in composed_bases_dict:
                        composed_bases_dict[composed_base] += k
                    else:
                        composed_bases_dict[composed_base] = k

                    for b in simple_bases:
                        sb_counter += k
                        if b in simple_bases_dict:
                            simple_bases_dict[b] += k
                        else:
                            simple_bases_dict[b] = k

        t2 = time()

        times.append(t2-t1)
        lengths.append(pow(2, j)*d_length)

    # plt.plot(lengths, times, "red")
    # plt.xlabel("length of dictionary")
    # plt.ylabel("time (s)")
    # plt.show()

def monte_carlo_sample(d, n, load=False):
    if load:
        d = pickle.load(open(d, "rb"))
    else:
        d = construct_dict(d)
    dico = { 'rockyou' : d}

    rdset.scores(10000000)

    gr.construct_grammar_model(dico)
    construct_time_test(d, "rockyou", 10)

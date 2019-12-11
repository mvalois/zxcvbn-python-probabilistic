import pickle
import random
import time
from threading import Thread

import probabilistic_models.grammar_utils as gru
from random import choice

class dthread(Thread):
    def __init__(self, cb_counter, sb_counter, composed_bases_dict ,simple_bases_dict, composed_bases_list, simple_bases_lists, n):
        super(dthread, self).__init__()
        self.cb_counter = cb_counter
        self.sb_counter = sb_counter
        self.composed_bases_dict = composed_bases_dict
        self.simple_bases_dict = simple_bases_dict
        self.composed_bases_list = composed_bases_list
        self.simple_bases_lists = simple_bases_lists
        self.n = n
        self.sco = []
    def run(self):
        for i in range(self.n // 100):
            print(i)
            ws = draw(self.cb_counter, self.simple_bases_dict, self.composed_bases_list, self.simple_bases_lists, 100)
            for w in ws:
                s = gru.score(w, self.cb_counter, self.sb_counter, self.composed_bases_dict, self.simple_bases_dict, self.simple_bases_lists)
                self.sco.append(s)

def draw(cb_counter, simple_bases_dict, composed_bases_list, simple_bases_lists, n):
    indexes = [random.randint(0, cb_counter) for _ in range(n)]
    words = []
    for cb_index in indexes:
        while cb_index not in composed_bases_list:
            cb_index += 1
        composed_base = composed_bases_list[cb_index]
        simple_bases = gru.cut(composed_base)
        word = ""
        for base in simple_bases:
            dico = simple_bases_lists[base]
            sb_index = random.randint(0, simple_bases_dict[base])
            while sb_index not in dico:
                sb_index += 1
            word += dico[sb_index]
        words.append(word)
    return words


def scores(n):
    (composed_bases_list, simple_bases_lists) = pickle.load(open("lists.p", "rb"))
    (cb_counter, composed_bases_dict) = pickle.load(open("cb_dictionary.p", "rb"))
    (sb_counter, simple_bases_dict) = pickle.load(open("sb_dictionary.p", "rb"))
    scores_list = []

    for i in range(n//100):
        print(i)
        ws = draw(cb_counter, simple_bases_dict, composed_bases_list, simple_bases_lists, 100)
        for w in ws:
            s = gru.score(w, cb_counter, sb_counter, composed_bases_dict, simple_bases_dict, simple_bases_lists)
            scores.append(s)
    # t1 = dthread(cb_counter, sb_counter, composed_bases_dict, simple_bases_dict, composed_bases_list,
    #              simple_bases_lists, n // 4)
    # t2 = dthread(cb_counter, sb_counter, composed_bases_dict, simple_bases_dict, composed_bases_list,
    #              simple_bases_lists, n // 4)
    # t3 = dthread(cb_counter, sb_counter, composed_bases_dict, simple_bases_dict, composed_bases_list,
    #              simple_bases_lists, n // 4)
    # t4 = dthread(cb_counter, sb_counter, composed_bases_dict, simple_bases_dict, composed_bases_list,
    #              simple_bases_lists, n // 4)
    #
    # t1.start()
    # t2.start()
    # t3.start()
    # t4.start()
    # t1.join()
    # t2.join()
    # t3.join()
    # t4.join()
    #
    # scores_list = t1.sco + t2.sco + t3.sco + t4.sco

    pickle.dump(scores_list, open("scores.p", "wb"))
    return

import pickle
import random
import bisect
import time

from . import grammar_utils as gru



def draw(cb_counter, cbo_list, cb_list, sb_dict, sbo_lists, sb_lists):
    r = random.randint(1, cb_counter)
    cb = cb_list[gru.dichotomy(cbo_list, r)]
    simple_bases = gru.cut(cb)
    word = ""
    for base in simple_bases:
        dico = sb_lists[base]
        r = random.randint(1, sb_dict[base])
        sup = gru.dichotomy(sbo_lists[base], r)
        inf = gru.dichotomy_inf(sbo_lists[base], r)
        word += dico[sup]
        sb_occurrences = sup - inf
    return word, sb_occurrences


def draw_score(cb_counter, sb_counter, cbo_list, cb_list, sb_dict, sbo_lists, sb_lists):
    r = random.randint(1, cb_counter)
    cb_sup = gru.dichotomy(cbo_list, r)
    cb_inf = gru.dichotomy_inf(cbo_list, r)
    cb = cb_list[cb_sup]
    s = (cb_sup-cb_inf)/cb_counter
    simple_bases = gru.cut(cb)
    word = ""
    for base in simple_bases:
        dico = sb_lists[base]
        r = random.randint(1, sb_dict[base])
        sb_sup = gru.dichotomy(sbo_lists[base], r)
        sb_inf = gru.dichotomy_inf(sbo_lists[base], r)
        word += dico[sb_sup]
        s *= (sb_sup-sb_inf)/sb_counter
    return s

def scores(n):
    (composed_bases_list, simple_bases_lists) = pickle.load(open("lists.p", "rb"))
    (cb_counter, composed_bases_dict) = pickle.load(open("cb_dictionary.p", "rb"))
    (sb_counter, simple_bases_dict) = pickle.load(open("sb_dictionary.p", "rb"))
    scores_list = []

    cbo_list = []
    sbo_lists = dict()
    
    for k in composed_bases_list:
        bisect.insort(cbo_list, k)
        simple_bases = gru.cut(composed_bases_list[k])
        for base in simple_bases:
            print(base)
            if not (base in sbo_lists):
                sbo_lists[base] = []
                for l in simple_bases_lists[base]:
                    bisect.insort(sbo_lists[base], l)
                print(sbo_lists[base])
    
    print(cbo_list)
    
    pickle.dump(cbo_list, open("cbo.p", "wb"))
    pickle.dump(sbo_lists, open("sbo.p", "wb"))

    # cbo_list = pickle.load(open("cbo.p", "rb"))
    # sbo_lists = pickle.load(open("sbo.p", "rb"))

    for i in range(n):
        if (i%10000)==0:
            print(i)
        scores_list.append(draw_score(cb_counter, sb_counter, cbo_list, composed_bases_list, simple_bases_dict, sbo_lists, simple_bases_lists))
    pickle.dump(scores_list, open("scores.p", "wb"))

    return

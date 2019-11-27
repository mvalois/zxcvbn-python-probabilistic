import probabilistic_models.grammar_utils as gru
from zxcvbn_functions.frequency_lists import FREQUENCY_LISTS
import pickle



def build_dict(list):
    d = dict()
    for w in list:
        if w in d:
            d[w] += 1
        else:
            d[w] = 1
    return d



FREQUENCY_DICTIONARIES = {}


def add_frequency_lists(frequency_lists_):
    for name, lst in frequency_lists_.items():
        FREQUENCY_DICTIONARIES[name] = build_dict(lst)


add_frequency_lists(FREQUENCY_LISTS)


def construct_grammar_model(_ranked_dictionaries=FREQUENCY_DICTIONARIES):
    composed_bases_dict = dict()
    simple_bases_dict = dict()
    composed_bases_list = dict()
    simple_bases_lists = dict()

    cb_counter = 0
    sb_counter = 0

    tmp_cb_dict = dict()
    tmp_sb_lists = dict()


    for dictionary_name, frequency_dict in _ranked_dictionaries.items():
        iter_verif = 0
        ll = len(frequency_dict)//100
        for w in frequency_dict:

            if w != "" :
                if iter_verif % ll == 0 : print(iter_verif//ll, '%')
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

    pickle.dump((cb_counter, composed_bases_dict), open("cb_dictionary.p", "wb"))
    pickle.dump((sb_counter, simple_bases_dict), open("sb_dictionary.p", "wb"))
    key = 0

    for cb in tmp_cb_dict:
        key += tmp_cb_dict[cb]
        composed_bases_list[key] = cb

    for cbp in tmp_sb_lists:
        key = 0
        simple_bases_lists[cbp] = {}
        for cb in tmp_sb_lists[cbp]:
            key += tmp_sb_lists[cbp][cb]
            simple_bases_lists[cbp][key] = cb

    pickle.dump((composed_bases_list, simple_bases_lists), open("lists.p", "wb"))

    return


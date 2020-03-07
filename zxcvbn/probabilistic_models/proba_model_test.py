import pickle
from . import grammar_utils as gru
from . import random_set as rs

from . import grammars
from .probabilistic_model import probabilistic_model_guesses

fl = {
    "1": "aaaaa123bb,ccc**azerty".split(","),
    "2": "123jaaj!,888abc320,320lll123".split(",")
}


def build_ranked_dict(ordered_list):
    return {word: idx for idx, word in enumerate(ordered_list, 1)}


RD = {}


def add_frequency_lists(frequency_lists_):
    for name, lst in frequency_lists_.items():
        RD[name] = build_ranked_dict(lst)


if __name__ == "__main__":

    add_frequency_lists(fl)
    # grammars.construct_grammar_model()
    # rs.scores(1000000)

    (cb_counter, Q) = pickle.load(open("cb_dictionary.p", "rb"))
    (sb_counter, B) = pickle.load(open("sb_dictionary.p", "rb"))

    print("cloudpasswordmoon" in B)
    print(gru.score("qwerty", cb_counter, sb_counter, Q, B))
    print(gru.score("abc123", cb_counter, sb_counter, Q, B))


    print(probabilistic_model_guesses("password"))

import pickle
from .grammar_utils import score, update
from decimal import Decimal


def probabilistic_model_guesses(password):
    (composed_bases_list, simple_bases_lists) = pickle.load(open("lists.p", "rb"))
    (cb_counter, composed_bases_dict) = pickle.load(open("cb_dictionary.p", "rb"))
    (sb_counter, simple_bases_dict) = pickle.load(open("sb_dictionary.p", "rb"))
    sbo_lists = pickle.load(open("sbo.p", "rb"))
    scores = pickle.load(open("scores.p", "rb"))
    score_password = score(password, cb_counter, sb_counter, composed_bases_dict, simple_bases_dict, simple_bases_lists, sbo_lists)
    len_score = len(scores)
    rank_password = 0
    for i in range(len_score):
        if scores[i] > score_password:
            rank_password += 1/(scores[i]*len_score)
    return int(rank_password)


def probabilistic_model_result(password):
    guesses = probabilistic_model_guesses(password)
    #update(password)
    return {
        "guesses" : Decimal(guesses),
        "sequence" : [],
        "password" : password,
        "pattern" : "probabilistic_model"
    }

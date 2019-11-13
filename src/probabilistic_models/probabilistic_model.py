import pickle
from src.probabilistic_models.grammar_utils import score, update
from math import log
from decimal import Decimal

def probabilistic_model_guesses(password):
    scores = pickle.load(open("scores.p", "rb"))
    (cb_counter, Q) = pickle.load(open("cb_dictionary.p", "rb"))
    (sb_counter, B) = pickle.load(open("sb_dictionary.p", "rb"))
    score_password = score(password, cb_counter, sb_counter, Q, B)
    len_score = len(scores)
    rank_password = 0
    for i in range(len_score) :
        if scores[i] > score_password :
            rank_password += 1/ (scores[i]*len_score)
    return int(rank_password)


def probabilistic_model_result(password):
    guesses = probabilistic_model_guesses(password)
    update(password)
    return {
        "guesses_log10" : log(guesses, 10),
        "guesses" : Decimal(guesses),
        "sequence" : [],
        "password" : password,
        "pattern" : "probabilistic_model"
    }

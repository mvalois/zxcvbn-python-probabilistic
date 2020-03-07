import pickle
from .grammar_utils import score, update
from .probabilistic_sample import monte_carlo_sample
from decimal import Decimal

MODEL=list()
SAMPLE=list()

def probabilistic_model_guesses(password, d, n):
    if not MODEL:
        MODEL, SAMPLE = monte_carlo_sample(d, n)
    (composed_bases_list, simple_bases_lists) = MODEL[0]
    (cb_counter, composed_bases_dict) = MODEL[1]
    (sb_counter, simple_bases_dict) = MODEL[2]
    sbo_lists = pickle.load(open("sbo.p", "rb"))
    score_password = score(password, cb_counter, sb_counter, composed_bases_dict, simple_bases_dict, simple_bases_lists, sbo_lists)
    len_score = len(SAMPLE)
    rank_password = 0
    for i in range(len_score):
        if SAMPLE[i] > score_password:
            rank_password += 1/(SAMPLE[i]*len_score)
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

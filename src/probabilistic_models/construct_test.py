import pickle
import src.probabilistic_models.grammars as gr


def construct_dict():
    f = open("rockyou-withcount-utf-8.txt", "r")
    i = 0
    d = dict()
    for l in f:
        i+=1
        n = int(l[0:8])
        w = l[8:-1]
        d[w] = n
        if i%1000 == 0:
            print(i)
            print((w,n))
    pickle.dump(d, open("rockyou_dictionary.p", "wb"))
    print(d)


# gr.construct_grammar_model()

(cb_counter, Q) = pickle.load(open("cb_dictionary.p", "rb"))
(sb_counter, B) = pickle.load(open("sb_dictionary.p", "rb"))
(l1,l2) = pickle.load(open("lists.p", "rb"))

print(l1)

d = pickle.load(open("rockyou_dictionary.p", "rb"))
dico = { 'truc' : d}

gr.construct_grammar_model(dico)
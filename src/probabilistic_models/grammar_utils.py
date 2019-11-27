import pickle

def cut(composed_base):
    res = []
    b = composed_base[0]
    for i in range(1, len(composed_base)):
        if composed_base[i].isdigit():
            b += composed_base[i]
        else:
            res.append(b)
            b = composed_base[i]
    res.append(b)
    return res
        
        
def bases(w) :
    simple_bases = []
    composed_base = ''
    word =''
    for c in w:
        if word == '': word = c
        elif char_type(word[-1]) == char_type(c):
            word += c
        else :
            simple_bases.append(word)
            composed_base += char_type(word[-1]) + str(len(word))
            word = c
    simple_bases.append(word)

    composed_base += char_type(word[-1]) + str(len(word))
    return simple_bases, composed_base


def char_type(c):
    if c.isdigit() : return 'D'
    elif c.isalpha(): return 'L'
    else : return 'S'

    
def score(w, cb_counter, sb_counter, composed_bases_dict, simple_bases_dict):
    B, Q = bases(w)
    S = 0
    if Q in composed_bases_dict:
        S = composed_bases_dict[Q]/cb_counter
    for b in B:
        if b in simple_bases_dict:
            S *= simple_bases_dict[b]/sb_counter
        else:
            S = 0
    return S

def update(password):
    T, Qw = bases(password)
    (cb_counter, Q) = pickle.load(open("cb_dictionary.p", "rb"))
    (sb_counter, B) = pickle.load(open("sb_dictionary.p", "rb"))

    if Qw in Q :
        Q[Qw] += 1
    else :
        Q[Qw] = 1
    cb_counter += 1

    for Tj in T :
        if Tj in B :
            B[Tj] += 1
        else :
            B[Tj] = 1
        sb_counter += 1

    pickle.dump((cb_counter, Q), open("cb_dictionary.p", "wb"))
    pickle.dump((sb_counter, B), open("sb_dictionary.p", "wb"))
    return

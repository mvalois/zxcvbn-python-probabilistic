import pickle

def dichotomy(li, e):
    inf = 0
    sup = len(li)
    med = sup//2
    if e >= li[-1]:
        return li[-1]
    while 1:
        if e > li[med]:
            if e <= li[med + 1]:
                return li[med + 1]
            inf = med
        else:
            if (med == 0) or (e > li[med - 1]):
                return li[med]
            sup = med
        med = (sup + inf) // 2


def dichotomy_inf(li, e):
    inf = 0
    sup = len(li)
    med = sup//2
    if e >= li[-1]:
        return li[-1]
    while 1:
        if e >= li[med]:
            if e <= li[med + 1]:
                return li[med]
            inf = med
        else:
            if med == 0:
                return 0
            if e >= li[med - 1]:
                return li[med - 1]
            sup = med
        med = (sup + inf) // 2

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


def score(w, cb_counter, sb_counter, composed_bases_dict, simple_bases_dict, simple_bases_list, sbo_lists):
    B, Q = bases(w)
    S = 0
    if Q in composed_bases_dict:
        S = composed_bases_dict[Q]/cb_counter
    simple_bases = cut(Q)
    for i in range(len(simple_bases)):
        p = simple_bases[i]
        b = B[i]
        if p in simple_bases_dict:
            d = simple_bases_list[p]
            nb_bases = 0
            for k, v in d.items():
                if v == b:
                    nb_bases = k - 1
                    break
            if nb_bases != 0:
                nb_bases = dichotomy_inf(sbo_lists[p], nb_bases)
                nb_bases = k - nb_bases
                S *= nb_bases/sb_counter
            else:
                return 0
        else:
            return 0
    return S


###
### à modifier
###
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

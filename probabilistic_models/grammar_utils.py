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

    
def score(w, composed_bases_dict, simple_bases_dict):
    B, Q = bases(w)
    S = 0
    if Q in composed_bases_dict:
        S = composed_bases_dict[Q]
    for b in B:
        if b in simple_bases_dict:
            S *= simple_bases_dict[b]
        else:
            S = 0
    return S
    
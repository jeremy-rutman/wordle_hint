from collections import defaultdict
from itertools import permutations
from matplotlib import pyplot as plt
import string 

def letter_frequencies(word_list):
    letter_freqs = defaultdict(int)
    for word in word_list:
        for letter in word:
            letter_freqs[letter]+=1
    return letter_freqs

def calc_probs(wordlist,lf):
    probs = []
    for word in wordlist:
        letters_seen = []
        s = 0
        for letter in word:
            if not letter in letters_seen:
                s+=lf[letter]
            letters_seen.append(letter)
        probs.append([word,s])
    probs = sorted([[word,s] for [word,s] in probs],key=lambda x:x[1],reverse=True)
    for i,p in enumerate(probs):
        print(probs[i])
        if i>2:
            break
    return(probs)

def find_candidates(wordlist,lf,eliminated_letters,correct_wrong_position,correct_right_position):
    candidate_words = wordlist
    for letter in eliminated_letters:
        candidate_words = [word for word in candidate_words if not letter in word] 
    print(len(candidate_words))
    for letter in correct_wrong_position:
        candidate_words = [word for word in candidate_words if letter in word] 
    print(len(candidate_words))
    for [letter,pos] in correct_right_position:
        candidate_words = [word for word in candidate_words if word[pos]==letter] 
    print(len(candidate_words))
    return candidate_words

with open('enable1.txt','r') as fp:
    words = fp.readlines()
    words = [w.replace('\n','') for w in words]
    words = [word for word in words if len(word)==5]
    print(f'{len(words)} five letter words')
    lf = letter_frequencies(words)
    tot_n = sum([v for v in lf.values()])
    lf = {k:v/tot_n for k,v in lf.items()}
    sorted_lf = sorted([[l,f] for l,f in lf.items()],key=lambda x:x[1],reverse=True)
    print(tot_n)
    print(lf)
    print(sorted_lf)
    calc_probs(words,lf)
    eliminated_letters = ['a','b','c']
    correct_wrong_position = ['l','i']
    correct_right_position = [['k',0]]
    candidates = find_candidates(words,lf,eliminated_letters,correct_wrong_position,correct_right_position)
    print(candidates)
    calc_probs(candidates,lf)
    print('kills' in words)

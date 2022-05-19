from collections import defaultdict
from itertools import permutations
#from matplotlib import pyplot as plt
import string 

# todo - best guess takes all known letters and puts them into 'wrong' basket 

class wordle():
    def __init__(self):
        with open('scrabble_official_enable1.txt', 'r') as fp:
            words = fp.readlines()
        words = [w.replace('\n', '') for w in words]
        words = [word for word in words if len(word) == 5]
        print(f'{len(words)} five letter words')
        self.worldlist = words
        lf = self.letter_frequencies(words)
        tot_n = sum([v for v in lf.values()])
        lf = {k: v / tot_n for k, v in lf.items()}
        self.lf = lf
        sorted_lf = sorted([[l, f] for l, f in lf.items()], key=lambda x: x[1], reverse=True)
        #    calc_probs(words,lf)
        hidden_word = 'kings'
        #    initial_guess = calc_probs(words,lf)
        #    el,cwp,crp = make_guess(initial_guess[0][0], hidden_word)
        self.solve_wordle(words, lf, hidden_word)


    def letter_frequencies(self,word_list):
        letter_freqs = defaultdict(int)
        for word in word_list:
            for letter in word:
                letter_freqs[letter]+=1
        return letter_freqs

    def calc_probs(self,wordlist,lf):
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

    def find_candidates(self,wordlist,lf,eliminated_letters,correct_wrong_position,correct_right_position):
        candidate_words = wordlist
        for letter in eliminated_letters:
            candidate_words = [word for word in candidate_words if not letter in word]
        for letter in correct_wrong_position:
            candidate_words = [word for word in candidate_words if letter in word]
        for [letter,pos] in correct_right_position:
            candidate_words = [word for word in candidate_words if word[pos]==letter]
        print(f'{len(candidate_words)} candidates found for: el {eliminated_letters} cwp {correct_wrong_position} crp {correct_right_position}')
        return candidate_words

    def find_forcing_guesses(self,wordlist,lf,eliminated_letters,cwp,crp):
        crp_letter_list = [rightpos[0] for rightpos in crp]
        prevent_all = eliminated_letters+cwp+crp_letter_list
        print('all together',prevent_all)
        candidates = self.find_candidates(wordlist,lf,prevent_all,[],[])
        if (candidates):
            print('found candidates with eliminated+cwp+crp')
            return(candidates)
        prevent_eliminated_cwp = eliminated_letters+cwp
        print('eliminated+cwp',prevent_eliminated_cwp)
        candidates = self.find_candidates(wordlist,lf,prevent_eliminated_cwp,[],[])
        if (candidates):
            print('found candidates with eliminated+cwp')
            return(candidates)
        prevent_eliminated_crp = eliminated_letters+crp_letter_list
        print('eliminated+crp',prevent_eliminated_crp)
        candidates = find_candidates(wordlist,lf,prevent_eliminated_crp,[],[])
        if (candidates):
            print('found candidates with eliminated+crp')
            return(candidates)
        print('eliminated',eliminated_letters)
        candidates = find_candidates(wordlist,lf,eliminated_letters,[],[])
        if (candidates):
            print('found candidates with eliminated only')
            return(candidates)
        else:
            print('no candidates found')
            return []

    def most_forcing_guess(self,wordlist,lf,elim,cwp,crp):
        candidates = self.find_forcing_guesses(wordlist,lf,elim,cwp,crp)
        probs = self.calc_probs(candidates,lf)
        if probs:
            return probs[0]
        return None

    def freq_plot(self,sorted_lf):
        plt.bar(range(26),[f[1] for f in sorted_lf])
        plt.xticks(range(26),[l[0] for l in sorted_lf])
        plt.title('letter frequencies amongst 5 letter words in official scrabble dictionary')
        plt.show()

    def solve_wordle(self,words,lf,hidden_word):
        print(f'solving wordle for {hidden_word}')
        correct_right_position,correct_wrong_position,eliminated_letters = [],[],[]
        while(len(correct_right_position))!=5:
            candidates = self.find_candidates(words,lf,eliminated_letters,correct_wrong_position,correct_right_position)
            self.calc_probs(candidates,lf)
            mfg = self.most_forcing_guess(words,lf,eliminated_letters,correct_wrong_position,correct_right_position)
            best_guess = mfg[0]
            print(f'best guesss {best_guess}')
            el,cwp,crp = self.make_guess(best_guess,hidden_word)
            eliminated_letters = list(set(eliminated_letters+el))
            correct_wrong_position = list(set(correct_wrong_position+cwp))
            print(f'oldcrp {correct_right_position} newcrp {crp}')
            new_crp = self.union_lists(correct_right_position,crp)
            print(f'updated crp {new_crp}')
            set_newcrp = set(new_crp)
            correct_right_position = list(set(correct_right_position+crp))
            print(f'el {eliminated_letters}, cwp {correct_wrong_position}, crp {correct_right_position}')
            input('rtc')

    def union_lists(self,l1,l2):
        result = []
        for e in l1:
            if e not in result:
                result.append(e)
        for e in l2:
            if e not in result:
                result.append(e)
        return result

    def make_guess(self,guess_word,hidden_word):
        print(f'guessing {guess_word} for {hidden_word}')
        correct_right_position,correct_wrong_position,eliminated_letters = [],[],[]
        for i,letter in enumerate(guess_word):
            if letter == hidden_word[i]:
                correct_right_position.append((letter,i))
            elif letter in hidden_word and letter not in correct_wrong_position:
                correct_wrong_position.append(letter)
            else:
                eliminated_letters.append(letter)
        return eliminated_letters,correct_wrong_position, correct_right_position

w = wordle()
print(w.lf['e'])

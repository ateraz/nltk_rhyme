import collections
import json

import nltk

from cache import cached_rhyme


class Rhyme(object):
    """ Rhymes for all pronunciations of word """

    # (word, pronunciation) list
    entries = nltk.corpus.cmudict.entries()
    vowels = 'AEIOU'

    def __init__(self, word, min_level=2, res_limit=50):
        self.word = word
        self.min_level = min_level
        self.res_limit = res_limit
        self.pronunciations = [p for w, p in self.entries if w == self.word]

    @cached_rhyme
    def __str__(self):
        res = []
        sorter = lambda x: x['level']
        for word in self.rhymes:
            res.append({
                'word': word,
                'rhymes': sorted(self.rhymes[word], key=sorter, reverse=True)[:self.res_limit]
            })
        return json.dumps({'data': res})

    def get_rhyme_pronunciation(self, pronunciation):
        """ Check if rhymes with pronunciation.
        Returns word pronunciation that rhymes """
        for p in self.pronunciations:
            if p[-self.min_level:] == pronunciation[-self.min_level:]:
                return p

    def get_rhyme_level(self, p1, p2):
        """ Returns count of last sounds that rhymes """
        l = min(len(p1), len(p2))
        for i in range(self.min_level + 1, l + 1):
            if p1[-i] != p2[-i]:
                return i - 1
        return max(self.min_level, l)

    @staticmethod
    def get_string_pronunciation(word, pronunciation):
        return '{0} [{1}]'.format(word, ' '.join(pronunciation).lower())

    @property
    def rhymes(self):
        rhymes = collections.defaultdict(list)
        if not self.pronunciations:
            return rhymes
        for word, pronunciation in self.entries:
            if word == self.word:
                continue
            rhyme_pronunciation = self.get_rhyme_pronunciation(pronunciation)
            if rhyme_pronunciation:
                level = self.get_rhyme_level(rhyme_pronunciation,
                                             pronunciation)
                key = self.get_string_pronunciation(self.word,
                                                    rhyme_pronunciation)
                rhymes[key].append({
                    'word': self.get_string_pronunciation(word, pronunciation),
                    'level': level
                })
        return dict(rhymes)

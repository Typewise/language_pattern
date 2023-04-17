#### PATTERN | XX | INFLECT ########################################################################
# -*- coding: utf-8 -*-
# Copyright (c)
# Author:
# License:
# http://www.clips.ua.ac.be/pages/pattern

####################################################################################################
# Template for pattern.xx.inflect with functions for word inflection in language XXXXX.
# inflection is the modification of a word to express different grammatical categories,
# such as tense, mood, voice, aspect, person, number, gender and case.
# Conjugation is the inflection of verbs.
# To construct a lemmatizer for pattern.xx.parser.find_lemmata(),
# we need functions for noun singularization, verb infinitives, predicate adjectives, etc.

from __future__ import unicode_literals
from __future__ import division

from builtins import str, bytes, dict, int
from builtins import map, zip, filter
from builtins import object, range

import os
import sys
import re

try:
    MODULE = os.path.dirname(os.path.realpath(__file__))
except:
    MODULE = ""

sys.path.insert(0, os.path.join(MODULE, "..", "..", "..", ".."))

# Import Verbs base class and verb tenses.
from pattern.text import Verbs as _Verbs
from pattern.text import (
    INFINITIVE, PRESENT, PAST, FUTURE,
    FIRST, SECOND, THIRD,
    SINGULAR, PLURAL, SG, PL,
    PROGRESSIVE,
    PARTICIPLE
)

sys.path.pop(0)

VERB, NOUN, ADJECTIVE, ADVERB = "VB", "NN", "JJ", "RB"

VOWELS = "aeiouy"
re_vowel = re.compile(r"a|e|i|o|u|y", re.I)
is_vowel = lambda ch: ch in VOWELS

#### ARTICLE #######################################################################################

# Inflection gender.
MASCULINE, FEMININE, NEUTER, PLURAL = \
    MALE, FEMALE, NEUTRAL, PLURAL = \
    M, F, N, PL = "m", "f", "n", "p"

# Definite articles.
DEFINITE_ARTICLES = ["o", "a", "os", "as"]

# Indefinite articles.
INDEFINITE_ARTICLES = ["um", "uma", "uns", "umas"]

plural_irregular = {
    "água": "águas",
    "alazão": "alazões",
    "alemão": "alemães",
    "álcool": "álcoois",
    "animal": "animais",
    "após": "após",
    "arroz": "arroz",
    "atlas": "atlas",
    "avião": "aviões",
    "bebê": "bebês",
    "bife": "bifes",
    "cão": "cães",
    "capitão": "capitães",
    "caráter": "caracteres",
    "cartaz": "cartazes",
    "chapéu": "chapéus",
    "chave": "chaves",
    "cônsul": "cônsules",
    "dó": "dólares",
    "escrivão": "escrivães",
    "fácil": "fáceis",
    "feijão": "feijões",
    "gás": "gases",
    "grão": "grãos",
    "hífen": "hifens",
    "irmão": "irmãos",
    "jardim": "jardins",
    "lã": "lãs",
    "lápis": "lápis",
    "mal": "males",
    "mão": "mãos",
    "mel": "meles",
    "mês": "meses",
    "mulher": "mulheres",
    "nariz": "narizes",
    "olho": "olhos",
    "ovo": "ovos",
    "pão": "pães",
    "papagaio": "papagaios",
    "pé": "pés",
    "peixe": "peixes",
    "pincel": "pincéis",
    "porco": "porcos",
    "projétil": "projéteis",
    "rato": "ratos",
    "réptil": "répteis",
    "rol": "roles",
    "sabão": "sabões",
    "sangue": "sangues",
    "sede": "sedes",
    "sofá": "sofás",
    "tênis": "tênis",
    "trem": "trens",
    "véu": "véus",
    "voo": "voos"
}
singular_irregular = dict((v, k) for k, v in plural_irregular.items())


def pluralize(word, pos=NOUN, custom={}):
    """Returns the plural of a given word."""

    if word in custom:
        return custom[word]
    word = word.lower()
    if word in plural_irregular:
        return plural_irregular[word]
    if word.endswith("ão"):
        return word[:-2] + "ões"
    elif word.endswith("l"):
        return word + "s"
    elif word.endswith("r") or word.endswith("z") or word.endswith("n"):
        return word + "es"
    elif word.endswith("m"):
        return word[:-1] + "ns"
    elif re.match(r"^(g|q)u", word):
        return word + "s"
    else:
        return word + "s"


def singularize(word, pos=NOUN, custom={}):
    """Returns the singular of a given word."""

    if word in custom:
        return custom[word]
    word = word.lower()
    if word in singular_irregular:
        return singular_irregular[word]

    if word.endswith("ões"):
        return word[:-3] + "ão"
    elif word.endswith("ais"):
        return word[:-1]
    elif word.endswith("eis"):
        return word[:-1]
    elif word.endswith("res"):
        return word[:-2]
    elif word.endswith("ns"):
        return word + "m"
    elif re.match(r"^(g|q)ue", word):
        return word[:-1]
    else:
        return word.rstrip("s")


def inflect_adjective(adjective, gender, number):
    """Inflects an adjective for gender and number."""
    if gender == MASCULINE:
        if number == SG:
            return adjective
        else:
            return adjective + "s"
    else:
        if number == SG:
            return re.sub(r"o$", "a", adjective)
        else:
            return re.sub(r"o$", "as", adjective)


#### VERB CONJUGATION ##############################################################################
# The verb table was trained on CELEX and contains the top 2000 most frequent verbs.


class Verbs(_Verbs):

    def __init__(self):
        _Verbs.__init__(self, os.path.join(MODULE, "pt-verbs.txt"),
                        language="pt",
                        # The order of tenses in the given file; see pattern.text.__init__.py => Verbs.
                        format=[0, 1, 2, 3, 4, 5, 6, 34, 35, 36, 37, 38, 39, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27,
                                28, 40, 41, 42, 43, 44, 45, 52, 55, 57, 58, 59, 60, 46, 47, 48, 49, 50, 51, 33, 33, 33,
                                33, 33, 33, 24, 24, 24, 24, 24, 24, 52, 52, 52, 52, 52, 52, 55, 55, 58, 54, 60, 55, 57,
                                58, 59, 60, 8, 24],
                        default={}
                        )

    def find_lemma(self, verb):
        """ Returns the base form of the given inflected verb, using a rule-based approach.
        """
        if verb.endswith("ar"):
            return verb[:-2]
        elif verb.endswith("er") or verb.endswith("ir"):
            return verb[:-2]
        else:
            return verb

    def find_lexeme(self, verb):
        """ For a regular verb (base form), returns the forms using a rule-based approach.
        """
        root = verb[:-2]
        if verb.endswith("ar"):
            endings = ["o", "as", "a", "amos", "ais", "am",
                       "ei", "aste", "ou", "amos", "astes", "aram",
                       "ava", "avas", "ava", "ávamos", "áveis", "avam",
                       "ara", "aras", "ara", "áramos", "áreis", "aram",
                       "asse", "asses", "asse", "ássemos", "ásseis", "assem",
                       "e", "es", "e", "emos", "eis", "em",
                       "aria", "arias", "aria", "aríamos", "aríeis", "ariam",
                       "eira", "eiras", "eira", "eiríamos", "eiríeis", "eiram",
                       "ando", "ado"]
        elif verb.endswith("er"):
            endings = ['o', 'es', 'e', 'emos', 'eis', 'em',  # 1
                       'i', 'este', 'eu', 'emos', 'estes', 'eram',  # 2
                       'ia', 'ias', 'ia', 'íamos', 'íeis', 'iam',  # 3
                       'era', 'eras', 'era', 'êramos', 'êreis', 'eram',  # 4
                       'erei', 'erás', 'erá', 'eremos', 'ereis', 'erão',  # NO
                       'a', 'as', 'a', 'amos', 'ais', 'am',  # 6
                       'esse', 'esses', 'esse', 'êssemos', 'êsseis', 'essem',  # 5
                       'er', 'eres', 'er', 'ermos', 'erdes', 'erem',
                       'er', 'eres', 'er', 'ermos', 'erdes', 'erem',
                       'eria', 'erias', 'eria', 'eríamos', 'eríeis', 'eriam',
                       'e', 'a', 'amos', 'e', 'am',
                       'as', 'a', 'amos', 'ais', 'am',
                       'endo', 'ido']

        else:
            # elif verb.endswith("ir"):
            endings = ['o', 'es', 'e', 'imos', 'is', 'em',  # 1
                       'i', 'iste', 'iu', 'imos', 'istes', 'iram',  # 2
                       'ia', 'ias', 'ia', 'íamos', 'íeis', 'iam',  # 3
                       'ira', 'iras', 'ira', 'íramos', 'íreis', 'iram',  # 4
                       'irei', 'irás', 'irá', 'iremos', 'ireis', 'irão',  # NO
                       'a', 'as', 'a', 'amos', 'ais', 'am',  # 6
                       'esse', 'esses', 'esse', 'êssemos', 'êsseis', 'essem',  # 5
                       'ir', 'ires', 'ir', 'irmos', 'irdes', 'irem',
                       'ir', 'ires', 'ir', 'irmos', 'irdes', 'irem',
                       'ia', 'ias', 'ia', 'iríamos', 'iríeis', 'iam',
                       'e', 'a', 'amos', 'i', 'am',
                       'as', 'a', 'amos', 'ais', 'am',
                       'indo', 'ido']

        return [root] + [root + e for e in endings]


verbs = Verbs()

conjugate, lemma, lexeme, tenses = \
    verbs.conjugate, verbs.lemma, verbs.lexeme, verbs.tenses


#### ATTRIBUTIVE & PREDICATIVE #####################################################################


def attributive(adjective):
    """ For a predicative adjective, returns the attributive form.
    """
    return adjective


def predicative(adjective):
    """ Returns the predicative adjective.
    """
    return adjective

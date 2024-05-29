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
    "alazão": "alazões",
    "alemão": "alemães",
    "álcool": "álcoois",
    "aldeão": "aldeãos",
    "anão": "anões",
    "ás": "ases",
    "atlas": "atlas",
    "avião": "aviões",
    "balcão": "balcões",
    "cão": "cães",
    "capelão": "capelães",
    "capitão": "capitães",
    "capitã": "capitãs",
    "caráter": "caracteres",
    "cartão": "cartões",
    "cidadão": "cidadãos",
    "cônsul": "cônsules",
    "cristão": "cristãos",
    "dor": "dores",
    "escrivão": "escrivães",
    "fácil": "fáceis",
    "feijão": "feijões",
    "frágil": "frágeis",
    "gás": "gases",
    "gel": "géis",
    "grão": "grãos",
    "guardião": "guardiães",
    "hífen": "hífenes",
    "homem": "homens",
    "incrível": "incríveis",
    "irmão": "irmãos",
    "irmã": "irmãs",
    "júnior": "juniores",
    "lã": "lãs",
    "lápis": "lápis",
    "leão": "leões",
    "mãe": "mães",
    "mal": "males",
    "mão": "mãos",
    "mel": "meles",
    "mês": "meses",
    "mulher": "mulheres",
    "nariz": "narizes",
    "olho": "olhos",
    "ônibus": "ônibus",
    "pão": "pães",
    "papagaio": "papagaios",
    "patrão": "patrões",
    "pé": "pés",
    "peixe": "peixes",
    "pincel": "pincéis",
    "projétil": "projéteis",
    "raiz": "raízes",
    "rato": "ratos",
    "réptil": "répteis",
    "rol": "róis",
    "sabão": "sabões",
    "sangue": "sangues",
    "sede": "sedes",
    "sênior": "seniores",
    "sofá": "sofás",
    "tênis": "tênis",
    "trem": "trens",
    "véu": "véus",
    "vírus": "vírus",
    "voo": "voos"
}
singular_irregular = dict((v, k) for k, v in plural_irregular.items())


def contains_accent(word):
    """Returns True if the given word contains an accentuated character."""
    return bool(re.search(r"[áéíóúâêîôûàèìòù]", word))


def pluralize(word, pos=NOUN, custom={}):
    """Returns the plural of a given word."""

    if word in custom:
        return custom[word]
    word = word.lower()
    if word in plural_irregular:
        return plural_irregular[word]
    if word.endswith("ão"):
        return word[:-2] + "ões"  # add exceptions to plural_irregular
    elif word.endswith("x") or word.endswith("us"):
        return word
    elif word.endswith("el") and not contains_accent(word):  # stress is on last syllable, needs accent to stay there
        return word[:-2] + "éis"
    elif word.endswith("ol"):
        return word[:-2] + "óis"
    elif word.endswith("il"):
        if contains_accent(word):
            return word[:-2] + "eis"
        else:
            return word[:-2] + "is"
    elif word.endswith("l"):
        return word[:-1] + "is"
    elif word.endswith("és") or word.endswith("ês"):
        return word[:-2] + "eses"
    elif word.endswith("r") or word.endswith("z") or word.endswith("s"):
        return word + "es"
    elif word.endswith("m"):
        return word[:-1] + "ns"
    else:
        return word + "s"


def singularize(word, pos=NOUN, custom={}):
    """Returns the singular of a given word."""

    if word in custom:
        return custom[word]
    word = word.lower()
    if word in singular_irregular:
        return singular_irregular[word]

    if word.endswith("ões") or word.endswith("ães") or word.endswith("ãos"):
        return word[:-3] + "ão"
    elif word.endswith("x") or word.endswith("us"):
        return word
    elif word.endswith("eis"):
        if contains_accent(word):
            return word[:-2] + "il"
        else:
            return word[:-2] + "el"
    elif word.endswith("ais") or word.endswith("uis"):
        return word[:-2] + "l"
    elif word.endswith("éis"):
        return word[:-3] + "el"
    elif word.endswith("óis"):
        return word[:-3] + "ol"
    elif word.endswith("is"):
        return word[:-1] + "l"
    elif word.endswith("res"):
        return word[:-2]
    elif word.endswith("ns"):
        return word[:-2] + "m"
    else:
        return word.rstrip("s")


def inflect_adjective(adjective, gender, number):
    """Inflects an adjective for gender and number."""
    # Handle irregular adjectives or exceptions
    irregular_adjectives = {
        'bom': {'MASCULINE': {'SG': 'bom', 'PL': 'bons'}, 'FEMININE': {'SG': 'boa', 'PL': 'boas'}},
        'mau': {'MASCULINE': {'SG': 'mau', 'PL': 'maus'}, 'FEMININE': {'SG': 'má', 'PL': 'más'}},
        'fácil': {'MASCULINE': {'SG': 'fácil', 'PL': 'fáceis'}, 'FEMININE': {'SG': 'fácil', 'PL': 'fáceis'}},
        'difícil': {'MASCULINE': {'SG': 'difícil', 'PL': 'difíceis'}, 'FEMININE': {'SG': 'difícil', 'PL': 'difíceis'}},
        'são': {'MASCULINE': {'SG': 'são', 'PL': 'sãos'}, 'FEMININE': {'SG': 'sã', 'PL': 'sãs'}},
    }
    if adjective in irregular_adjectives:
        return irregular_adjectives[adjective][gender][number]

    # Regular inflection patterns
    if gender == MASCULINE:
        if number == SG:
            return adjective
        else:
            # Special handling for -l, -m, -r, -s, -z endings
            if adjective.endswith("il"):
                return re.sub(r"il$", "is", adjective)
            elif adjective.endswith("l"):
                return re.sub(r"l$", "is", adjective)
            elif adjective.endswith("m"):
                return re.sub(r"m$", "ns", adjective)
            elif adjective.endswith(("r", "z")):
                return adjective + "es"
            elif adjective.endswith("ês"):
                return re.sub(r"ês$", "eses", adjective)  # Correctly handle -ês to -eses
            return adjective if adjective.endswith("s") else adjective + "s"
    else:
        if number == SG:
            if adjective.endswith("o"):
                return re.sub(r"o$", "a", adjective)
            return adjective
        else:
            if adjective.endswith("o"):
                return re.sub(r"o$", "as", adjective)
            # Special handling for -l, -m, -r, -s, -z, -ês endings
            if adjective.endswith("il"):
                return re.sub(r"il$", "is", adjective)
            elif adjective.endswith("l"):
                return re.sub(r"l$", "is", adjective)
            elif adjective.endswith("m"):
                return re.sub(r"m$", "ns", adjective)
            elif adjective.endswith(("r", "z")):
                return adjective + "es"
            elif adjective.endswith("ês"):
                return re.sub(r"ês$", "eses", adjective)  # Correctly handle -ês to -eses
            return adjective if adjective.endswith("s") else adjective + "s"


#### VERB CONJUGATION ##############################################################################
# The verb table was trained on CELEX and contains the top 2000 most frequent verbs.


class Verbs(_Verbs):

    def __init__(self):
        _Verbs.__init__(self, os.path.join(MODULE, "pt-verbs.txt"),
                        language="pt",
                        # The order of tenses in the given file; see pattern.text.__init__.py => Verbs.
                        format=[
                            0, 1, 2, 3, 4, 5, 6,
                            34, 35, 36, 37, 38, 39,
                            17, 18, 19, 20, 21, 22,
                            40, 41, 42, 43, 44, 45,
                            55, 56, 57, 58, 59, 60,
                            67, 68, 69, 70, 71, 72,
                            46, 47, 48, 49, 50, 51,
                            52, 8, 24],
                        default={}
                        )

    def find_lemma(self, verb):
        """Returns the base form of the given inflected Portuguese verb."""
        v = verb.lower()
        # Handle common irregular verb forms directly.
        irregular_verbs = {
            'sou': 'ser', 'és': 'ser', 'é': 'ser', 'somos': 'ser', 'sois': 'ser', 'são': 'ser',
            'estou': 'estar', 'estás': 'estar', 'está': 'estar', 'estamos': 'estar', 'estais': 'estar',
            'estão': 'estar',
            'fui': 'ser', 'foi': 'ser', 'fomos': 'ser', 'foram': 'ser',
            'tenho': 'ter', 'tens': 'ter', 'tem': 'ter', 'temos': 'ter', 'tendes': 'ter', 'têm': 'ter',
            'digo': 'dizer', 'diz': 'dizer', 'dizemos': 'dizer', 'dizeis': 'dizer', 'dizem': 'dizer',
            'faço': 'fazer', 'faz': 'fazer', 'fazemos': 'fazer', 'fazeis': 'fazer', 'fazem': 'fazer',
            'seja': 'ser', 'sejas': 'ser', 'sejamos': 'ser', 'sejam': 'ser',
            'vou': 'ir', 'vais': 'ir', 'vai': 'ir', 'vamos': 'ir', 'ides': 'ir', 'vão': 'ir',
            'venho': 'vir', 'vens': 'vir', 'vem': 'vir', 'vimos': 'vir', 'vindes': 'vir', 'vêm': 'vir',
            'vejo': 'ver', 'vês': 'ver', 'vê': 'ver', 'vemos': 'ver', 'vedes': 'ver', 'veem': 'ver',
            'dou': 'dar', 'dás': 'dar', 'dá': 'dar', 'damos': 'dar', 'dais': 'dar', 'dão': 'dar',
            'sei': 'saber', 'sabes': 'saber', 'sabe': 'saber', 'sabemos': 'saber', 'sabeis': 'saber', 'sabem': 'saber',
            'posso': 'poder', 'podes': 'poder', 'pode': 'poder', 'podemos': 'poder', 'podeis': 'poder',
            'podem': 'poder',
            'saio': 'sair', 'sais': 'sair', 'sai': 'sair', 'saímos': 'sair', 'saís': 'sair', 'saem': 'sair',
            'trago': 'trazer', 'trazes': 'trazer', 'traz': 'trazer', 'trazemos': 'trazer', 'trazeis': 'trazer',
            'trazem': 'trazer',
            'caio': 'cair', 'cais': 'cair', 'cai': 'cair', 'caímos': 'cair', 'caís': 'cair', 'caem': 'cair',
            'leio': 'ler', 'lês': 'ler', 'lê': 'ler', 'lemos': 'ler', 'ledes': 'ler', 'leem': 'ler',
            # Add more irregular forms as needed.
        }
        if v in irregular_verbs:
            return irregular_verbs[v]
        # Regular verb endings handling.
        if v.endswith(("ar", "er", "ir")):
            return v
        # Infinitive by removing common verb suffixes and applying the most probable infinitive ending.
        suffixes = (
            ("ava", "ar"), ("ia", "er"), ("iu", "ir"), ("eu", "er"),  # Imperfect and simple past
            ("ando", "ar"), ("endo", "er"), ("indo", "ir"),  # Gerund
            ("ado", "ar"), ("ido", ["er", "ir"]),  # Past participle
            ("o", "ar"), ("e", "er"), ("e", "ir"),  # Present indicative
            ("am", "ar"), ("em", ["er", "ir"]),  # Present indicative plural
        )
        for suffix, infinitive_ending in suffixes:
            if v.endswith(suffix):
                base = v[:-len(suffix)]
                if isinstance(infinitive_ending, list):  # Choose between -er and -ir based on the verb stem.
                    if base[-1] in "aeiou":
                        return base + infinitive_ending[0]  # Prefer -er for vowel-ending stems.
                    else:
                        return base + infinitive_ending[1]  # Prefer -ir otherwise.
                return base + infinitive_ending
        # If no rule matched, return the verb as is (might be already in infinitive or an irregular form not covered).
        return v

    def find_lexeme(self, verb):
        """Generates conjugated forms for a given Portuguese verb (regular or irregular)."""
        # Expanded list of some common irregular verbs with a selection of their forms.
        irregular_verbs = {
            'ser': ['sou', 'és', 'é', 'somos', 'sois', 'são', 'fui', 'foste', 'foi', 'fomos', 'foram', 'era', 'eras',
                    'éramos', 'eram', 'serei', 'serás', 'será', 'seremos', 'serão', 'seja', 'sejas', 'sejamos',
                    'sejam'],
            'ter': ['tenho', 'tens', 'tem', 'temos', 'têm', 'tive', 'tiveste', 'teve', 'tivemos', 'tiveram', 'tinha',
                    'tinhas', 'tínhamos', 'tinham', 'terei', 'terás', 'terá', 'teremos', 'terão', 'tenha', 'tenhas',
                    'tenhamos', 'tenham'],
            'ir': ['vou', 'vais', 'vai', 'vamos', 'vão', 'fui', 'foste', 'foi', 'fomos', 'foram', 'ia', 'ias', 'íamos',
                   'iam', 'irei', 'irás', 'irá', 'iremos', 'irão', 'vá', 'vás', 'vamos', 'vão'],
            'vir': ['venho', 'vens', 'vem', 'vimos', 'vêm', 'vim', 'vieste', 'veio', 'viemos', 'vieram', 'vinha',
                    'vinhas', 'vínhamos', 'vinham', 'virei', 'virás', 'virá', 'viremos', 'virão', 'venha', 'venhas',
                    'venhamos', 'venham'],
            'estar': ['estou', 'estás', 'está', 'estamos', 'estão', 'estive', 'estiveste', 'esteve', 'estivemos',
                      'estiveram', 'estava', 'estavas', 'estávamos', 'estavam', 'estarei', 'estarás', 'estará',
                      'estaremos', 'estarão', 'esteja', 'estejas', 'estejamos', 'estejam'],
            'fazer': ['faço', 'fazes', 'faz', 'fazemos', 'fazem', 'fiz', 'fizeste', 'fez', 'fizemos', 'fizeram',
                      'fazia', 'fazias', 'fazíamos', 'faziam', 'farei', 'farás', 'fará', 'faremos', 'farão', 'faça',
                      'faças', 'façamos', 'façam'],
            'dizer': ['digo', 'dizes', 'diz', 'dizemos', 'dizem', 'disse', 'disseste', 'disse', 'dissemos', 'disseram',
                      'dizia', 'dizias', 'dizíamos', 'diziam', 'direi', 'dirás', 'dirá', 'diremos', 'dirão', 'diga',
                      'digas', 'digamos', 'digam'],
            'poder': ['posso', 'podes', 'pode', 'podemos', 'podeis', 'podem', 'pude', 'pudeste', 'pôde', 'pudemos',
                      'puderam', 'podia', 'podias', 'podíamos', 'podiam', 'poderei', 'poderás', 'poderá', 'poderemos',
                      'poderão', 'possa', 'possas', 'possamos', 'possam'],
            'saber': ['sei', 'sabes', 'sabe', 'sabemos', 'sabeis', 'sabem', 'soube', 'soubeste', 'soube', 'soubemos',
                      'souberam', 'sabia', 'sabias', 'sabíamos', 'sabiam', 'saberei', 'saberás', 'saberá', 'saberemos',
                      'saberão', 'saiba', 'saibas', 'saibamos', 'saibam'],
            'dar': ['dou', 'dás', 'dá', 'damos', 'dais', 'dão', 'dei', 'deste', 'deu', 'demos', 'deram', 'dava',
                    'davas', 'dávamos', 'davam', 'darei', 'darás', 'dará', 'daremos', 'darão', 'dê', 'dês', 'dêmos',
                    'deem'],
            'ler': ['leio', 'lês', 'lê', 'lemos', 'leis', 'leem', 'li', 'leste', 'leu', 'lemos', 'leram', 'lia', 'lias',
                    'líamos', 'liam', 'lerei', 'lerás', 'lerá', 'leremos', 'lerão', 'leia', 'leias', 'leiamos',
                    'leiam'],
            'ver': ['vejo', 'vês', 'vê', 'vemos', 'vedes', 'veem', 'vi', 'viste', 'viu', 'vimos', 'viram', 'via',
                    'vias', 'víamos', 'viam', 'verei', 'verás', 'verá', 'veremos', 'verão', 'veja', 'vejas', 'vejamos',
                    'vejam'],
            # Add more irregular verbs as needed.
        }

        # Check if the verb is irregular and return its forms if found.
        if verb in irregular_verbs:
            return [verb] + irregular_verbs[verb]

        # Check if the verb is regular or irregular.
        if not verb.endswith(("ar", "er", "ir")):
            raise ValueError("Verb must end in 'ar', 'er', or 'ir'.")

        root = verb[:-2]

        if verb.endswith("ar"):
            endings = ["o", "as", "a", "amos", "ais", "am",
                       "ei", "aste", "ou", "amos", "astes", "aram",
                       "ava", "avas", "ava", "ávamos", "áveis", "avam",
                       "ara", "aras", "ara", "áramos", "áreis", "aram",
                       "asse", "asses", "asse", "ássemos", "ásseis", "assem",
                       "e", "es", "e", "emos", "eis", "em",
                       "aria", "arias", "aria", "aríamos", "aríeis", "ariam",
                       "ando", "ado"]
        elif verb.endswith("er"):
            endings = ["o", "es", "e", "emos", "eis", "em",
                       "i", "este", "eu", "emos", "estes", "eram",
                       "ia", "ias", "ia", "íamos", "íeis", "iam",
                       "era", "eras", "era", "êramos", "êreis", "eram",
                       "erei", "erás", "erá", "eremos", "ereis", "erão",
                       "a", "as", "a", "amos", "ais", "am",
                       "esse", "esses", "esse", "êssemos", "êsseis", "essem",
                       "endo", "ido"]
        else:  # verb.endswith("ir")
            endings = ["o", "es", "e", "imos", "is", "em",
                       "i", "iste", "iu", "imos", "istes", "iram",
                       "ia", "ias", "ia", "íamos", "íeis", "iam",
                       "ira", "iras", "ira", "íramos", "íreis", "iram",
                       "irei", "irás", "irá", "iremos", "ireis", "irão",
                       "a", "as", "a", "amos", "ais", "am",
                       "isse", "isses", "isse", "íssemos", "ísseis", "issem",
                       "indo", "ido"]

        forms = [root + e for e in endings]

        return forms


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

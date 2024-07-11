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

from tw_python_utils.logger.logging_initialiser import LOGGER
LOGGER.setLevel("WARNING")

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
GENDER = ["m", "f", "n", "p"]

# Definite articles.
DEFINITE_ARTICLES = ["o", "a", "os", "as"]

# Indefinite articles.
INDEFINITE_ARTICLES = ["um", "uma", "uns", "umas"]


def definite_article(word, gender=MALE):
    """ Returns the definite article (o/a/os/as) for a given word.
    """
    if MASCULINE in gender:
        return "os" if PLURAL in gender else "o"
    return "as" if PLURAL in gender else "a"


def indefinite_article(word, gender=MALE):
    """ Returns the indefinite article (um/uma/uns/umas) for a given word.
    """
    if MASCULINE in gender:
        return "uns" if PLURAL in gender else "um"
    return "umas" if PLURAL in gender else "uma"


DEFINITE = "definite"
INDEFINITE = "indefinite"


def article(word, function=INDEFINITE, gender=MALE):
    """ Returns the indefinite (um) or definite (o) article for the given word.
    """
    return function == DEFINITE \
       and definite_article(word, gender) \
        or indefinite_article(word, gender)
_article = article


def referenced(word, article=INDEFINITE, gender=MALE):
    """ Returns a string with the article + the word.
    """
    return "%s %s" % (_article(word, article, gender), word)


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


#### GENDER #########################################################################################

def gender(word):
    """Returns the gender for the given word, either:
       MALE, FEMALE, (MALE, FEMALE), (MALE, PLURAL) or (FEMALE, PLURAL)."""

    w = word.lower()

    exceptions = {
        'dor': FEMALE,
        'flor': FEMALE,
        'cor': FEMALE,
        'mar': MALE,
        'luz': FEMALE,
        'paz': FEMALE,
        'sol': MALE,
        'mel': MALE,
        'calor': MALE,
        'mãe': FEMALE,
        'pai': MALE,
        'árvore': FEMALE,
        'noite': FEMALE,
        'fome': FEMALE,
        'sede': FEMALE,
        'voz': FEMALE,
        'vez': FEMALE,
        'foto': FEMALE,
        'mão': FEMALE,
        'lei': FEMALE,
        'série': FEMALE,
        'equipe': FEMALE,
        'reunião': FEMALE,
        'sistema': MALE,
        'problema': MALE,
        'análise': FEMALE,
        'decisão': FEMALE,
        'ação': FEMALE,
        'dia': MALE,
        'mapa': MALE,
        'clima': MALE,
        'planeta': MALE,
        'tema': MALE,
        'programa': MALE,
        'idioma': MALE,
        'paixão': FEMALE,
        'questão': FEMALE,
        'opinião': FEMALE,
        'religião': FEMALE,
        'reflexão': FEMALE,
        'sugestão': FEMALE,
        'transgressão': FEMALE,
        'transmissão': FEMALE,
        'união': FEMALE,
        'versão': FEMALE,
        'visão': FEMALE,
    }

    # Check for exceptions first
    if w in exceptions:
        return exceptions[w]

    # Handling specific and common endings
    if w.endswith(("a", "ade", "ção")):
        return FEMALE
    if w.endswith(("o", "ote", "or")):
        return MALE
    if w.endswith(("e", "l")):
        return (MALE, FEMALE)
    if w.endswith("ão"):
        # Consider adding logic to handle exceptions or ambiguous cases
        return MALE
    if w.endswith("as"):
        return (FEMALE, PLURAL)
    if w.endswith("os"):
        return (MALE, PLURAL)
    if w.endswith("ões"):
        # Return both possibilities for "ões" due to ambiguity
        return (MALE, FEMALE, PLURAL)

    # Default case for adjectives that apply to both genders
    return (MALE, FEMALE)


#### VERB CONJUGATION ##############################################################################

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
            'estou': 'estar', 'estás': 'estar', 'está': 'estar', 'tá': 'estar', 'estamos': 'estar', 'estais': 'estar',
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
            ("ava", "ar"), ("ia", "er"), ("iu", "ir"), ("eu", "er"), ("ou", "ar"), # Imperfect and simple past
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
            'ser': ['sou', 'és', 'é', 'somos', 'sois', 'são',
                    'fui', 'foste', 'foi', 'fomos', 'fostes', 'foram',
                    'era', 'eras', 'era', 'éramos', 'éreis', 'eram',
                    'serei', 'serás', 'será', 'seremos', 'sereis', 'serão',
                    'seja', 'sejas', 'seja', 'sejamos', 'sejais', 'sejam'],
            'ter': ['tenho', 'tens', 'tem', 'temos', 'tendes', 'têm',
                    'tive', 'tiveste', 'teve', 'tivemos', 'tivestes', 'tiveram',
                    'tinha', 'tinhas', 'tinha', 'tínhamos', 'tínheis', 'tinham',
                    'terei', 'terás', 'terá', 'teremos', 'tereis', 'terão',
                    'tenha', 'tenhas', 'tenha', 'tenhamos', 'tenhais', 'tenham'],
            'ir': ['vou', 'vais', 'vai', 'vamos', 'ides', 'vão',
                   'fui', 'foste', 'foi', 'fomos', 'fostes', 'foram',
                   'ia', 'ias', 'ia', 'íamos', 'íeis', 'iam',
                   'irei', 'irás', 'irá', 'iremos', 'ireis', 'irão',
                   'vá', 'vás', 'vá', 'vamos', 'vades', 'vão'],
            'vir': ['venho', 'vens', 'vem', 'vimos', 'vindes', 'vêm',
                    'vim', 'vieste', 'veio', 'viemos', 'viestes', 'vieram',
                    'vinha', 'vinhas', 'vinha', 'vínhamos', 'vínheis', 'vinham',
                    'virei', 'virás', 'virá', 'viremos', 'vireis', 'virão',
                    'venha', 'venhas', 'venha', 'venhamos', 'venhais', 'venham'],
            'estar': ['estou', 'estás', 'está', 'estamos', 'estais', 'estão',
                      'estive', 'estiveste', 'esteve', 'estivemos', 'estivestes', 'estiveram',
                      'estava', 'estavas', 'estava', 'estávamos', 'estáveis', 'estavam',
                      'estarei', 'estarás', 'estará', 'estaremos', 'estareis', 'estarão',
                      'esteja', 'estejas', 'esteja', 'estejamos', 'estejais', 'estejam'],
            'fazer': ['faço', 'fazes', 'faz', 'fazemos', 'fazeis', 'fazem',
                      'fiz', 'fizeste', 'fez', 'fizemos', 'fizestes', 'fizeram',
                      'fazia', 'fazias', 'fazia', 'fazíamos', 'fazíeis', 'faziam',
                      'farei', 'farás', 'fará', 'faremos', 'fareis', 'farão',
                      'faça', 'faças', 'faça', 'façamos', 'façais', 'façam'],
            'dizer': ['digo', 'dizes', 'diz', 'dizemos', 'dizeis', 'dizem',
                      'disse', 'disseste', 'disse', 'dissemos', 'dissestes', 'disseram',
                      'dizia', 'dizias', 'dizia', 'dizíamos', 'dizíeis', 'diziam',
                      'direi', 'dirás', 'dirá', 'diremos', 'direis', 'dirão',
                      'diga', 'digas', 'diga', 'digamos', 'digais', 'digam'],
            'poder': ['posso', 'podes', 'pode', 'podemos', 'podeis', 'podem',
                      'pude', 'pudeste', 'pôde', 'pudemos', 'pudestes', 'puderam',
                      'podia', 'podias', 'podia', 'podíamos', 'podíeis', 'podiam',
                      'poderei', 'poderás', 'poderá', 'poderemos', 'podereis', 'poderão',
                      'possa', 'possas', 'possa', 'possamos', 'possais','possam'],
            'saber': ['sei', 'sabes', 'sabe', 'sabemos', 'sabeis', 'sabem',
                      'soube', 'soubeste', 'soube', 'soubemos', 'soubestes', 'souberam',
                      'sabia', 'sabias', 'sabia', 'sabíamos', 'sabíeis', 'sabiam',
                      'saberei', 'saberás', 'saberá', 'saberemos', 'sabereis', 'saberão',
                      'saiba', 'saibas', 'saiba', 'saibamos', 'saibais', 'saibam'],
            'dar': ['dou', 'dás', 'dá', 'damos', 'dais', 'dão',
                    'dei', 'deste', 'deu', 'demos', 'destes', 'deram',
                    'dava', 'davas', 'dava', 'dávamos', 'dáveis', 'davam',
                    'darei', 'darás', 'dará', 'daremos', 'dareis', 'darão',
                    'dê', 'dês', 'dê', 'dêmos', 'dai', 'dêem'],
            'ler': ['leio', 'lês', 'lê', 'lemos', 'leis', 'leem',
                    'li', 'leste', 'leu', 'lemos', 'lestes', 'leram',
                    'lia', 'lias', 'lia', 'líamos', 'líeis', 'liam',
                    'lerei', 'lerás', 'lerá', 'leremos', 'lereis', 'lerão',
                    'leia', 'leias', 'leia', 'leiamos', 'leiais', 'leiam'],
            'ver': ['vejo', 'vês', 'vê', 'vemos', 'vedes', 'veem',
                    'vi', 'viste', 'viu', 'vimos', 'vistes', 'viram',
                    'via', 'vias', 'via', 'víamos', 'víeis', 'viam',
                    'verei', 'verás', 'verá', 'veremos', 'vereis', 'verão',
                    'veja', 'vejas', 'veja', 'vejamos', 'vejais', 'vejam'],
            'querer': ['quero', 'queres', 'quer', 'queremos', 'quereis', 'querem',
                       'quis', 'quiseste', 'quis', 'quisemos', 'quisestes', 'quiseram',
                       'queria', 'querias', 'queria', 'queríamos', 'queríeis', 'queriam',
                       'quererei', 'quererás', 'quererá', 'quereremos', 'querereis', 'quererão',
                       'queira', 'queiras', 'queira', 'queiramos', 'queirais', 'queiram'],
            'pôr': ['ponho', 'pões', 'põe', 'pomos', 'pondes', 'põem',
                    'pus', 'puseste', 'pôs', 'pusemos', 'pusestes', 'puseram',
                    'punha', 'punhas', 'punha', 'púnhamos', 'púnheis', 'punham',
                    'porei', 'porás', 'porá', 'poremos', 'poreis', 'porão',
                    'ponha', 'ponhas', 'ponha', 'ponhamos', 'ponhais', 'ponham'],
            'opor': ['oponho', 'opões', 'opõe', 'opomos', 'opondes', 'opõem',
                     'opus', 'opuseste', 'opôs', 'opusemos', 'opusestes', 'opuseram',
                     'opunha', 'opunhas', 'opunha', 'opúnhamos', 'opúnheis', 'opunham',
                     'oporei', 'oporás', 'oporá', 'oporemos', 'oporeis', 'oporão',
                     'oponha', 'oponhas', 'oponha', 'oponhamos', 'oponhais', 'oponham'],
            'compor': ['componho', 'compões', 'compõe', 'compomos', 'compondes', 'compõem',
                       'compus', 'compuseste', 'compôs', 'compusemos', 'compusestes', 'compuseram',
                       'compunha', 'compunhas', 'compunha', 'compúnhamos', 'compúnheis', 'compunham',
                       'comporei', 'comporás', 'comporá', 'comporemos', 'comporeis', 'comporão',
                       'componha', 'componhas', 'componha', 'componhamos', 'componhais', 'componham'],
            'dispor': ['disponho', 'dispões', 'dispõe', 'dispomos', 'dispondes', 'dispõem',
                       'dispus', 'dispuseste', 'dispôs', 'dispusemos', 'dispusestes', 'dispuseram',
                       'dispunha', 'dispunhas', 'dispunha', 'dispúnhamos', 'dispúnheis', 'dispunham',
                       'disporei', 'disporás', 'disporá', 'disporemos', 'disporeis', 'disporão',
                       'disponha', 'disponhas', 'disponha', 'disponhamos', 'disponhais', 'disponham'],
            'propor': ['proponho', 'propões', 'propõe', 'propomos', 'propondes', 'propõem',
                       'propus', 'propuseste', 'propôs', 'propusemos', 'propusestes', 'propuseram',
                       'propunha', 'propunhas', 'propunha', 'propúnhamos', 'propúnheis', 'propunham',
                       'proporei', 'proporás', 'proporá', 'proporemos', 'proporeis', 'proporão',
                       'proponha', 'proponhas', 'proponha', 'proponhamos', 'proponhais', 'proponham'],
            'expor': ['exponho', 'expões', 'expõe', 'expomos', 'expondes', 'expõem',
                      'expus', 'expuseste', 'expôs', 'expusemos', 'expusestes', 'expuseram',
                      'expunha', 'expunhas', 'expunha', 'expúnhamos', 'expúnheis', 'expunham',
                      'exporei', 'exporás', 'exporá', 'exporemos', 'exporeis', 'exporão',
                      'exponha', 'exponhas', 'exponha', 'exponhamos', 'exponhais', 'exponham'],
            'depor': ['deponho', 'depões', 'depõe', 'depomos', 'depondes', 'depõem',
                      'depus', 'depuseste', 'depôs', 'depusemos', 'depusestes', 'depuseram',
                      'depunha', 'depunhas', 'depunha', 'depúnhamos', 'depúnheis', 'depunham',
                      'deporei', 'deporás', 'deporá', 'deporemos', 'deporeis', 'deporão',
                      'deponha', 'deponhas', 'deponha', 'deponhamos', 'deponhais', 'deponham'],
            'repor': ['reponho', 'repões', 'repõe', 'repomos', 'repondes', 'repõem',
                      'repus', 'repuseste', 'repôs', 'repusemos', 'repusestes', 'repuseram',
                      'repunha', 'repunhas', 'repunha', 'repúnhamos', 'repúnheis', 'repunham',
                      'reporei', 'reporás', 'reporá', 'reporemos', 'reporeis', 'reporão',
                      'reponha', 'reponhas', 'reponha', 'reponhamos', 'reponhais', 'reponham'],
            'supor': ['suponho', 'supões', 'supõe', 'supomos', 'supondes', 'supõem',
                      'supus', 'supuseste', 'supôs', 'supusemos', 'supusestes', 'supuseram',
                      'supunha', 'supunhas', 'supunha', 'supúnhamos', 'supúnheis', 'supunham',
                      'suporei', 'suporás', 'suporá', 'suporemos', 'suporeis', 'suporão',
                      'suponha', 'suponhas', 'suponha', 'suponhamos', 'suponhais', 'suponham'],
            # Add more irregular verbs as needed.
        }

        # Check if the verb is irregular and return its forms if found.
        if verb in irregular_verbs:
            return [verb] + irregular_verbs[verb]

        # Check if the verb is regular or irregular.
        if not verb.endswith(("ar", "er", "ir")):
            LOGGER.warning(f"UNKNOWN VERB: Verb must end in 'ar', 'er', or 'ir'. Verb: {verb}")

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

def attributive(adjective, gender=MALE):
    w = adjective.lower()
    # normal => normais
    if PLURAL in gender and w.endswith("l"):
        return w[:-1] + "is"
    if PLURAL in gender and w.endswith("ês"):
        return w[:-2] + "eses"
    if PLURAL in gender and w.endswith("m"):
        return w[:-1] + "ns"
    if PLURAL in gender and w.endswith("r", "z", "s"):
        return w + "es"
    if PLURAL in gender and w.endswith(("a", "e")):
        return w + "s"
    if w.endswith("o"):
        if FEMININE in gender and PLURAL in gender:
            return w[:-1] + "as"
        if FEMININE in gender:
            return w[:-1] + "a"
        if PLURAL in gender:
            return w + "s"
    return w


def predicative(adjective):
    """ Returns the predicative adjective (lowercase).
        In Portuguese, the attributive form is always used for descriptive adjectives:
        "el chico alto" => masculine,
        "la chica alta" => feminine.
        The predicative is useful for lemmatization.
    """
    w = adjective.lower()
    # histéricos => histérico
    if w.endswith(("os", "as")):
        w = w[:-1]
    # histérico => histérico
    if w.endswith("o"):
        return w
    # histérica => histérico
    if w.endswith("a"):
        return w[:-1] + "o"
    # felizes => feliz, ingleses => inglês, interessantes => interessante
    if w.endswith("es"):
        if w.endswith("eses"):
            return w[:-4] + "ês"
        if w.endswith(("zes", "res")):
            return w[:-2]
        else:
            return w[:-2] + "e"
    return w

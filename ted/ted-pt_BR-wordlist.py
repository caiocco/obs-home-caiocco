#!/usr/bin/python3
# -*- coding: utf-8 -*-
#
# ted-pt_BR-wordlist.py -- word list for Ted's pt_BR.dfa from VERO
#
# To the extent possible under law, the author has waived all copyright
# and related or neighboring rights to this file (CC0 1.0).
#
# Usage: ted-pt_BR-wordlist.py pt_BR.aff pt_BR.dic > words.txt
#
# VERO's pt_BR.dic was built with an aggressive "munch": many nouns are
# folded into unrelated stems (país = paí/B, mesa = meso/D, internet =
# net/Í, casa/janela/sistema = verbs casar, janelar, sistemar), and a
# full expansion yields ~10.5 million forms polluted by hyphenated
# enclisis, truncated verb forms (cantamo, fazê), pre-AO90 spellings
# and rare stems from Cândido de Figueiredo (1913).  This script keeps
# the stems that look like real Brazilian vocabulary, using the size of
# each morphological family as evidence, and expands only the useful
# affix classes.  The output is sorted, unique, one UTF-8 word per line.

import re
import sys
from collections import defaultdict

WARN_FLAGS = set("Ýý~")
SFX_ALLOWED = set("ABCDFHJKMOPRVXabcdetfghijtuw2")
VERB_FLAGS = set("abcdefhi")
RAW_VERB_FLAGS = {"ajkLMY", "ajkLY", "ejLMoY", "ajkLM", "ejLoY"}
RARE_NOUN_FLAGS = {"13DK", "DK", "BK", "3B", "13D", "123DK"}
ACCENTED = set("áàâãéêíóôõú")

LUSI_WHITELIST = {
    "pacto", "impacto", "compacto", "contacto", "intacto", "factível",
    "factual", "apto", "optar", "rapto", "cacto", "sectário", "convicção",
    "ficção", "fricção", "infecção", "secção", "opção", "recepção",
    "concepção", "percepção", "decepção", "exceção", "intersecção",
    "bisseção", "bissecção", "dissecção", "dissecar", "nupcial", "egípcio",
    "eucalipto", "bactéria",
}

ROOT_SUFFIX = re.compile(
    r"(?:zeir[oa]s?|zais|zal|zinh[oa]s?|inh[oa]s?|amentos?|imentos?|ações"
    r"|ições|ções|sões|dades?|eiros?|eiras?|arias?|ad[oa]s?|id[oa]s?"
    r"|áveis|íveis|ável|ível|iv[oa]s?|istas?|ismos?|ic[oa]s?|íssim[oa]s?"
    r"|mente|agens?|agem|ezas?|ices?|ud[oa]s?|ent[oa]s?|ot[ea]s?|et[ea]s?"
    r"|it[oa]s?|eir[oa]s?|os[oa]s?|dores?|doras?|tõ?es|sõ?es|çõ?es|ões|ães"
    r"|ais|éis|óis|uis|anos?|anas?|enses?|eses?|esas?|ar|er|ir|or|al|el|il"
    r"|ol|ul|ão|ã|as?|os?|es?|s)$")
UNACCENT = str.maketrans("áàâãéêíóôõúü", "aaaaeeiooouu")


def get_root(w):
    r = w.lower()
    if len(r) >= 4:
        r = ROOT_SUFFIX.sub("", r)
    if r.endswith("qu"):
        r = r[:-2] + "c"
    elif r.endswith("gu"):
        r = r[:-2] + "g"
    r = r.translate(UNACCENT)
    if len(r) >= 3:
        return r
    return w.lower()[:3].translate(UNACCENT)


def read_dic(path):
    entries = []
    with open(path, encoding="utf-8") as f:
        first = True
        for line in f:
            line = line.strip().lstrip("﻿")
            if first:
                first = False
                if line.isdigit():
                    continue
            if not line or line.startswith("#"):
                continue
            word, _, flags = line.partition("/")
            flags = flags.split()[0] if flags.strip() else ""
            if " " in word or "\t" in word:
                continue
            if WARN_FLAGS & set(flags):
                continue
            entries.append((word, flags))
    return entries


def hun_cond(cond, suffix):
    if cond == ".":
        return None
    pat = re.compile(("(?:%s)$" if suffix else "^(?:%s)") % cond)
    return pat


def read_aff(path):
    sfx = defaultdict(list)
    pfx = defaultdict(list)
    with open(path, encoding="utf-8") as f:
        for line in f:
            p = line.split()
            if len(p) < 5 or p[0] not in ("SFX", "PFX"):
                continue
            kind, flag, strip, add, cond = p[:5]
            strip = "" if strip == "0" else strip
            add, _, cont = add.partition("/")
            add = "" if add == "0" else add
            if "-" in add:
                continue
            if kind == "SFX":
                if flag not in SFX_ALLOWED:
                    continue
                if flag in VERB_FLAGS:
                    if strip in ("ar", "er", "or") and add in ("á", "ê", "ô"):
                        continue
                    if add.endswith("mo") or "díssim" in add:
                        continue
                sfx[flag].append((strip, add, cont, hun_cond(cond, True)))
            else:
                pfx[flag].append((strip, add, cont, hun_cond(cond, False)))
    return sfx, pfx


def apply_sfx(word, rules):
    for strip, add, cont, cond in rules:
        if strip and not word.endswith(strip):
            continue
        if cond is not None and not cond.search(word):
            continue
        yield (word[:len(word) - len(strip)] if strip else word) + add, cont


def apply_pfx(word, rules):
    for strip, add, cont, cond in rules:
        if strip and not word.startswith(strip):
            continue
        if cond is not None and not cond.search(word):
            continue
        yield add + word[len(strip):]


def main():
    if len(sys.argv) != 3:
        sys.exit("usage: %s pt_BR.aff pt_BR.dic" % sys.argv[0])
    sfx, pfx = read_aff(sys.argv[1])
    entries = read_dic(sys.argv[2])

    # 1. Families, hyphenated compounds as an oracle
    compound_parts = set()
    root_counts = defaultdict(int)
    root_flags = defaultdict(set)
    plain = []
    for stem, flags in entries:
        if "-" in stem:
            for part in stem.split("-"):
                if len(part) >= 2:
                    compound_parts.add(part.lower())
                    root_counts[get_root(part)] += 1
            continue
        r = get_root(stem)
        root_counts[r] += 1
        root_flags[r].update(flags)
        plain.append((stem, flags, r))

    # 2. Lusitanian / pre-AO90 duplicates
    all_stems = {s for s, _, _ in plain}
    lusi_drop = set()
    for stem, _, _ in plain:
        if stem in LUSI_WHITELIST:
            continue
        for old, new in (("ct", "t"), ("cç", "ç"), ("pt", "t"), ("pç", "ç")):
            if old in stem and stem.replace(old, new) in all_stems:
                lusi_drop.add(stem)
                break
        if "arquitect" in stem or "factor" in stem or stem == "facto":
            lusi_drop.add(stem)

    # 3. Stem filter
    kept = []
    nominal_only_verbs = []
    for stem, flags, r in plain:
        if stem in lusi_drop:
            continue
        if (stem.endswith("zinho") or stem.endswith("zinha")) and len(stem) > 6:
            continue
        s_low = stem.lower()
        is_comp = (s_low in compound_parts
                   or (s_low.endswith("o") and s_low[:-1] + "a" in compound_parts)
                   or (s_low.endswith("ar")
                       and (s_low[:-2] + "a" in compound_parts
                            or s_low[:-2] + "o" in compound_parts)))
        n = root_counts[r]
        if flags in RAW_VERB_FLAGS and n <= 3:
            if (n >= 2 or is_comp) and stem.endswith("ar"):
                nominal_only_verbs.append(stem)
            continue
        if (len(stem) <= 3 or is_comp
                or (len(stem) <= 5 and ACCENTED & set(stem))):
            keep = True
        elif len(flags) >= 2:
            keep = not (flags in RARE_NOUN_FLAGS and n <= 3)
        elif len(flags) == 0:
            keep = n >= 2 or len(stem) <= 6
        else:
            keep = n >= 4 and len(root_flags[r]) >= 3
        if keep:
            kept.append((stem, flags))

    # 4. Expansion
    out = set()
    for stem, flags in kept:
        forms = {stem}
        for fl in flags:
            if fl not in sfx:
                continue
            for w, cont in apply_sfx(stem, sfx[fl]):
                forms.add(w)
                for cf in cont:
                    if cf in sfx:
                        for w2, _ in apply_sfx(w, sfx[cf]):
                            forms.add(w2)
        # Prefixes go on the bare stem only: crossing them with the
        # suffixes adds ~400k junk forms (desaviadorezões, ...)
        pforms = set()
        for fl in flags:
            if fl in pfx:
                pforms.update(apply_pfx(stem, pfx[fl]))
        out.update(forms)
        out.update(pforms)
    for stem in nominal_only_verbs:
        base = stem[:-2]
        for end in ("o", "a", "os", "as", "ado", "ada", "ados", "adas"):
            out.add(base + end)

    out = sorted(w for w in out if w and "-" not in w)
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()

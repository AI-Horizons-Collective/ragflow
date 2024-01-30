import re

from nltk import word_tokenize

from rag.nlp import stemmer, huqie


def callback__(progress, msg, func):
    if not func :return
    func(progress, msg)


BULLET_PATTERN = [[
        r"第[零一二三四五六七八九十百]+编",
        r"第[零一二三四五六七八九十百]+章",
        r"第[零一二三四五六七八九十百]+节",
        r"第[零一二三四五六七八九十百]+条",
        r"[\(（][零一二三四五六七八九十百]+[\)）]",
    ], [
        r"[0-9]{,3}[\. 、]",
        r"[0-9]{,2}\.[0-9]{,2}",
        r"[0-9]{,2}\.[0-9]{,2}\.[0-9]{,2}",
        r"[0-9]{,2}\.[0-9]{,2}\.[0-9]{,2}\.[0-9]{,2}",
    ], [
        r"[零一二三四五六七八九十百]+[ 、]",
        r"[\(（][零一二三四五六七八九十百]+[\)）]",
        r"[\(（][0-9]{,2}[\)）]",
    ] ,[
        r"PART (ONE|TWO|THREE|FOUR|FIVE|SIX|SEVEN|EIGHT|NINE|TEN)",
        r"Chapter (I+V?|VI*|XI|IX|X)",
        r"Section [0-9]+",
        r"Article [0-9]+"
    ]
    ]


def bullets_category(sections):
    global BULLET_PATTERN
    hits = [0] * len(BULLET_PATTERN)
    for i, pro in enumerate(BULLET_PATTERN):
        for sec in sections:
            for p in pro:
                if re.match(p, sec):
                    hits[i] += 1
                    break
    maxium = 0
    res = -1
    for i,h in enumerate(hits):
        if h <= maxium:continue
        res = i
        maxium = h
    return res

def is_english(texts):
    eng = 0
    for t in texts:
        if re.match(r"[a-zA-Z]", t.strip()):
            eng += 1
    if eng / len(texts) > 0.8:
        return True
    return False

def tokenize(d, t, eng):
    d["content_with_weight"] = t
    if eng:
        t = re.sub(r"([a-z])-([a-z])", r"\1\2", t)
        d["content_ltks"] = " ".join([stemmer.stem(w) for w in word_tokenize(t)])
    else:
        d["content_ltks"] = huqie.qie(t)
        d["content_sm_ltks"] = huqie.qieqie(d["content_ltks"])
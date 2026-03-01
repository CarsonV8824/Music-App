import spacy

NLP = spacy.load("en_core_web_sm")

# ----------------------------
# Sensory Lexicon (Imagery)
# ----------------------------
VISUAL = {
    "dark", "light", "bright", "shadow", "blue", "red",
    "gold", "silver", "shine", "glow", "spark",
    "black", "white", "sky", "sun"
}

AUDITORY = {
    "whisper", "scream", "cry", "echo", "silence",
    "song", "sound", "loud", "quiet"
}

TACTILE = {
    "cold", "warm", "hot", "soft", "hard",
    "rough", "smooth", "burn", "freeze"
}

OLFACTORY = {"smell", "perfume", "smoke", "scent"}
GUSTATORY = {"sweet", "bitter", "sour", "taste"}

SENSORY_WORDS = (
    VISUAL |
    AUDITORY |
    TACTILE |
    OLFACTORY |
    GUSTATORY
)

# ----------------------------
# Helper Functions
# ----------------------------

def get_repetition_rate(text: str) -> float:
    lines = [
        line.strip().lower()
        for line in text.split("\n")
        if line.strip()
    ]

    if not lines:
        return 0.0

    unique_lines = set(lines)
    repetition_rate = 1 - (len(unique_lines) / len(lines))

    return max(0.0, repetition_rate)


def detect_imagery(doc) -> int:
    count = 0
    for token in doc:
        if (
            token.lemma_.lower() in SENSORY_WORDS
            and token.pos_ in {"NOUN", "VERB", "ADJ"}
        ):
            count += 1
    return count


def detect_similes(doc) -> int:
    # basic simile detection: "like a", "as ... as"
    similes = 0
    for i in range(len(doc) - 1):
        if doc[i].text.lower() == "like":
            similes += 1
        if (
            doc[i].text.lower() == "as"
            and doc[i+1].pos_ in {"ADJ", "ADV"}
        ):
            similes += 1
    return similes


def detect_anaphora(text: str) -> int:
    lines = [
        line.strip().lower()
        for line in text.split("\n")
        if line.strip()
    ]

    count = 0
    for i in range(len(lines) - 1):
        if lines[i].split()[:2] == lines[i+1].split()[:2]:
            count += 1

    return count


def detect_alliteration(doc) -> int:
    count = 0
    for i in range(len(doc) - 1):
        if (
            doc[i].is_alpha and doc[i+1].is_alpha and
            doc[i].text[0].lower() == doc[i+1].text[0].lower()
        ):
            count += 1
    return count


# ----------------------------
# MAIN ANALYZER
# ----------------------------

def analyze_lyrics(song_text: str) -> dict:

    if not song_text.strip():
        return {}

    doc = NLP(song_text)
    sents = list(doc.sents)

    words = [t.text.lower() for t in doc if t.is_alpha]
    total_words = len(words)

    if total_words == 0:
        return {}

    # ---------------- Lexical Diversity ----------------
    unique_words = len(set(words))
    raw_ttr = unique_words / total_words
    length_factor = min(1.0, total_words / 100)
    ttr = raw_ttr * length_factor

    # ---------------- Sentence Length ----------------
    avg_sentence_length = (
        sum(len([t for t in s if t.is_alpha]) for s in sents) / len(sents)
        if sents else 0.0
    )

    # ---------------- Syntactic Depth ----------------
    depths = []
    for sent in sents:
        token_depths = [len(list(token.ancestors)) for token in sent]
        if token_depths:
            depths.append(max(token_depths))

    syntactic_depth = (
        sum(depths) / len(depths)
        if depths else 0.0
    )

    # ---------------- Repetition ----------------
    repetition_rate = get_repetition_rate(song_text)

    # ---------------- Imagery ----------------
    imagery_count = detect_imagery(doc)
    imagery_density = imagery_count / total_words

    # ---------------- Literary Devices ----------------
    similes = detect_similes(doc)
    anaphora = detect_anaphora(song_text)
    alliteration = detect_alliteration(doc)

    device_total = similes + anaphora + alliteration
    literary_density = device_total / total_words

    # ---------------- Final Composite Score ----------------
    score = (
        0.25 * min(1.0, ttr) +
        0.15 * min(1.0, avg_sentence_length / 20) +
        0.15 * min(1.0, syntactic_depth / 10) +
        0.15 * min(1.0, imagery_density * 5) +
        0.15 * min(1.0, literary_density * 5) +
        0.15 * (1 - repetition_rate)
    )

    return {
        "score": round(score, 4),
        "ttr": round(ttr, 4),
        "avg_sentence_length": round(avg_sentence_length, 4),
        "syntactic_depth": round(syntactic_depth, 4),
        "imagery_density": round(imagery_density, 4),
        "literary_density": round(literary_density, 4),
        "repetition_rate": round(repetition_rate, 4),
        "similes": similes,
        "anaphora": anaphora,
        "alliteration": alliteration
    }
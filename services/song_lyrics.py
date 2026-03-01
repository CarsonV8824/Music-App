import spacy

NLP = spacy.load("en_core_web_sm")

def analyze_lyrics(song_text: str) -> float:
    if not song_text.strip():
        return 0.0

    doc = NLP(song_text)
    sents = list(doc.sents)

    # ---- Words ----
    words = [t.text.lower() for t in doc if t.is_alpha]
    if not words:
        return 0.0

    # ---- Lexical Diversity (TTR with soft length normalization) ----
    unique_words = len(set(words))
    total_words = len(words)

    raw_ttr = unique_words / total_words

    # Dampening factor for short texts
    length_factor = min(1.0, total_words / 100)
    ttr = raw_ttr * length_factor

    # ---- Sentence Length ----
    avg_sentence_length = (
        sum(len(s) for s in sents) / len(sents)
        if sents else 0.0
    )

    # ---- Syntactic Depth ----
    depths = []
    for sent in sents:
        token_depths = [len(list(token.ancestors)) for token in sent]
        if token_depths:
            depths.append(max(token_depths))

    syntactic_depth = (
        sum(depths) / len(depths)
        if depths else 0.0
    )

    # ---- Normalized Final Score ----
    score = (
        0.40 * min(1.0, ttr) +
        0.30 * min(1.0, avg_sentence_length / 20) +
        0.30 * min(1.0, syntactic_depth / 10)
    )

    return round(score, 4)

if __name__ == "__main__":
    with open("testing/lyrics.txt", "r") as f:
        lines = f.read()
    print(analyze_lyrics(lines))
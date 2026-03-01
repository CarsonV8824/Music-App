import spacy
NLP = spacy.load("en_core_web_sm")

def analyze_lyrics(song_text):
    global NLP
    doc = NLP(song_text)

    words = [t.text.lower() for t in doc if t.is_alpha]
    ttr = len(set(words)) / len(words)

    avg_sentence_length = sum(len(sent) for sent in doc.sents) / len(list(doc.sents))

    depths = []
    for sent in doc.sents:
        depths.append(max(len(list(token.ancestors)) for token in sent))

    syntactic_depth = sum(depths) / len(depths)

    ttr = len(set(words)) / len(words) if words else 0.0
    sents = list(doc.sents)
    avg_sentence_length = sum(len(s) for s in sents) / len(sents) if sents else 0.0
    depths = [max(len(list(t.ancestors)) for t in s) for s in sents if len(s)]
    syntactic_depth = sum(depths) / len(depths) if depths else 0.0

    score = (
        0.4 * min(1.0, ttr) +
        0.3 * min(1.0, avg_sentence_length / 20) +
        0.3 * min(1.0, syntactic_depth / 10)
    )   
    return score

if __name__ == "__main__":
    with open("lyrics.txt", "r") as f:
        text = f.read()
    print(analyze_lyrics(text))
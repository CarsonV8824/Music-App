from services.song_chords import analyze_chords
from services.song_lyrics import analyze_lyrics

from services.machine_learning import get_score_of_lyrics_from_model

def get_score_of_song(lyrics:str | None = None, chords:str | None = None) -> dict[str, float]:
    # Prefer provided inputs; fall back to local files.
    chord_text = chords
    if not chord_text:
        raise ValueError("No Chords")

    lyric_text = lyrics
    if not lyric_text:
        raise ValueError("no Lyrics in here")

    chord_percentage = analyze_chords(chord_text)
    lyric_percentage = get_score_of_lyrics_from_model(lyric_text)
    
    CHORD_WEIGHT = 0.7
    LYRIC_WEIGHT = 0.3
    score = (CHORD_WEIGHT * chord_percentage) + (LYRIC_WEIGHT * lyric_percentage)
    score = round(score, 2)
    bands = {
        "low": range(0, 40, 1), 
        "fair": range(40, 60, 1), 
        "good": range(60, 75, 1),
        "strong": range(75, 90, 1),
        "excellent": range(90, 101, 1)
    }

    for key, value in bands.items():
        if score * 100 in value:
            return f"score: {score} which is a {key} song."
    return score
    

if __name__ == "__main__":
    print(get_score_of_song("hello darkness", "C E G G#"))

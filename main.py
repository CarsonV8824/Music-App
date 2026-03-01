from song_chords import analyze_chords
from song_lyrics import analyze_lyrics

def get_score_of_song(lyrics:str, chords:str | None = None) -> float:
    # Prefer provided inputs; fall back to local files.
    chord_text = chords
    if chord_text is None:
        with open("chords.txt", "r") as f:
            chord_text = f.read()

    lyric_text = lyrics
    if not lyric_text:
        with open("lyrics.txt", "r") as f:
            lyric_text = f.read()

    chord_percentage = analyze_chords(chord_text)
    lyric_percentage = analyze_lyrics(lyric_text)

    # Keep lyrics influential without letting them over-penalize strong harmony.
    lyric_percentage = max(0.45, lyric_percentage)

    CHORD_WEIGHT = 0.75
    LYRIC_WEIGHT = 0.25
    return (CHORD_WEIGHT * chord_percentage) + (LYRIC_WEIGHT * lyric_percentage)
    

if __name__ == "__main__":
    print(get_score_of_song("test"))

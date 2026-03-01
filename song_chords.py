import numpy as np

def get_circle_of_fifths_distance(chord1: str, chord2: str) -> int:
    
    circle = [
        "C", "G", "D", "A", "E", "B",
        "F#", "C#", "Ab", "Eb", "Bb", "F"
    ]

    enharmonic_map = {
        "Db": "C#",
        "Gb": "F#",
        "Cb": "B",
        "Fb": "E",
        "E#": "F",
        "B#": "C",
        "G#": "Ab",
        "D#": "Eb",
        "A#": "Bb",
    }

    def extract_root(chord: str) -> str:
        if chord[:2] in enharmonic_map:
            return enharmonic_map[chord[:2]]
        if chord[:2] in circle:
            return chord[:2]
        if chord[:1] in enharmonic_map:
            return enharmonic_map[chord[:1]]
        return chord[:1]

    root1 = extract_root(chord1)
    root2 = extract_root(chord2)

    pos1 = circle.index(root1)
    pos2 = circle.index(root2)

    distance = abs(pos1 - pos2)

    return min(distance, 12 - distance)

def analyze_chords(text:str) -> float:
    "Analyzes the chord structure. every chord needs to have a space in the data. Return a float between 0 and 1"
    text = text.lstrip()
    text = text.rstrip()
    chords = text.split(" ")

    unique_chords = set(chords)

    # Repetition is normal in songs; discount repeat penalty instead of using a strict unique/total ratio.
    unique_count = len(unique_chords)
    repeat_count = len(chords) - unique_count
    unique_chords_ratio = unique_count / (unique_count + (0.35 * repeat_count)) if chords else 0

    CHORD_EXTENSION_NUMS = [6,7,9,11,13]
    CHORD_SYMBOLS = ["/", "sus4", "sus2", "sus", "aug", "dim","","minmaj"]
    complexity_of_chords = 0
    # max here is 5 * number of chords
    for chord in chords:
        for num in CHORD_EXTENSION_NUMS:
            if chord.count(str(num)) >= 1:
                match num:
                    case 6: complexity_of_chords += 2
                    case 7: complexity_of_chords += 2
                    case 9: complexity_of_chords += 3
                    case 11: complexity_of_chords += 4
                    case 13: complexity_of_chords += 5
            else:
                complexity_of_chords += 1
        for sym in CHORD_SYMBOLS:
            if chord.count(sym) > 1:
                match sym:
                    case "/": complexity_of_chords += 1
                    case "sus": complexity_of_chords += 1
                    case "sus4": complexity_of_chords += 1
                    case "sus2": complexity_of_chords += 1
                    case "minmaj": complexity_of_chords += 1
                    case "aug": complexity_of_chords += 2
                    case "dim": complexity_of_chords += 2
            else:
                pass

    # getting stats on next cord in sequence
    
    scores = []
    for index, chord in enumerate(chords):
        one_index_back = index - 1
        two_index_back = index - 2
        three_index_back = index - 3
        
        one_index_forward = index + 1
        two_index_forward = index + 2
        three_index_forward = index + 3

        if one_index_back >= 0:
            one_last_word = chords[one_index_back]
            scores.append(get_circle_of_fifths_distance(one_last_word, chord))

        if two_index_back >= 0:
            two_last_word = chords[two_index_back]
            scores.append(get_circle_of_fifths_distance(two_last_word, chord))

        if three_index_back >= 0:
            three_last_word = chords[three_index_back]
            scores.append(get_circle_of_fifths_distance(three_last_word, chord))
        
        if one_index_forward < len(chords):
            one_forward_chord = chords[one_index_forward]
            scores.append(get_circle_of_fifths_distance(one_forward_chord, chord))
        
        if two_index_forward < len(chords):
            two_forward_chord = chords[two_index_forward]
            scores.append(get_circle_of_fifths_distance(two_forward_chord, chord))

        if three_index_forward < len(chords):
            three_forward_chord = chords[three_index_forward]
            scores.append(get_circle_of_fifths_distance(three_forward_chord, chord))

    chord_structure = sum(scores)
    # Normalize by the number of pairwise comparisons actually collected.
    chord_structure = chord_structure / (len(scores) * 6) if scores else 0

    WEIGHT_UNIQUE = 0.15
    WEIGHT_COMPLEXITY = 0.50
    WEIGHT_STRUCTURE = 0.35

    score = (
        (WEIGHT_UNIQUE * min(1.0, unique_chords_ratio)) +
        (WEIGHT_COMPLEXITY * min(1.0, (complexity_of_chords / (len(chords) * 7)))) +
        (WEIGHT_STRUCTURE * min(1.0, chord_structure))
    )

    # Bonus for longer progressions with recurring material (sectional form).
    length_factor = min(1.0, max(0, len(chords) - 12) / 32)
    repeat_factor = min(1.0, repeat_count / max(1, int(len(chords) * 0.4)))
    form_bonus = 0.15 * length_factor * repeat_factor

    return min(1.0, score + form_bonus)
if __name__ == "__main__":
    with open("chords.txt", "r") as f:
        file = f.read()

    print(analyze_chords(file))

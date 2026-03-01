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


def analyze_chords(text: str) -> float:
    "Analyzes chord structure. Chords must be separated by spaces. Returns a float between 0 and 1."
    chords = [c for c in text.strip().split() if c]
    if not chords:
        return 0.0

    unique_chords = set(chords)

    # Repetition is normal in songs; discount repeat penalty instead of using a strict unique/total ratio.
    unique_count = len(unique_chords)
    repeat_count = len(chords) - unique_count
    unique_chords_ratio = unique_count / (unique_count + (0.35 * repeat_count))

    chord_extension_nums = [6, 7, 9, 11, 13]
    chord_symbols = ["/", "sus4", "sus2", "sus", "aug", "dim", "minmaj"]
    complexity_of_chords = 0

    # Complexity max target is len(chords) * 7 in the weighted normalization below.
    for chord in chords:
        for num in chord_extension_nums:
            if str(num) in chord:
                match num:
                    case 6:
                        complexity_of_chords += 2
                    case 7:
                        complexity_of_chords += 2
                    case 9:
                        complexity_of_chords += 3
                    case 11:
                        complexity_of_chords += 4
                    case 13:
                        complexity_of_chords += 5
            else:
                complexity_of_chords += 1

        for sym in chord_symbols:
            if sym in chord:
                match sym:
                    case "/":
                        complexity_of_chords += 1
                    case "sus" | "sus4" | "sus2" | "minmaj":
                        complexity_of_chords += 1
                    case "aug" | "dim":
                        complexity_of_chords += 2

    # Gather pairwise distances up to 3 positions away.
    scores = []
    for index, chord in enumerate(chords):
        one_index_back = index - 1
        two_index_back = index - 2
        three_index_back = index - 3

        one_index_forward = index + 1
        two_index_forward = index + 2
        three_index_forward = index + 3

        if one_index_back >= 0:
            scores.append(get_circle_of_fifths_distance(chords[one_index_back], chord))
        if two_index_back >= 0:
            scores.append(get_circle_of_fifths_distance(chords[two_index_back], chord))
        if three_index_back >= 0:
            scores.append(get_circle_of_fifths_distance(chords[three_index_back], chord))

        if one_index_forward < len(chords):
            scores.append(get_circle_of_fifths_distance(chords[one_index_forward], chord))
        if two_index_forward < len(chords):
            scores.append(get_circle_of_fifths_distance(chords[two_index_forward], chord))
        if three_index_forward < len(chords):
            scores.append(get_circle_of_fifths_distance(chords[three_index_forward], chord))

    # Normalize by number of pairwise comparisons actually collected.
    chord_structure = (sum(scores) / (len(scores) * 6)) if scores else 0.0

    weight_unique = 0.15
    weight_complexity = 0.50
    weight_structure = 0.35

    score = (
        (weight_unique * min(1.0, unique_chords_ratio)) +
        (weight_complexity * min(1.0, (complexity_of_chords / (len(chords) * 7)))) +
        (weight_structure * min(1.0, chord_structure))
    )

    # Bonus for longer progressions with recurring material (sectional form).
    length_factor = min(1.0, max(0, len(chords) - 12) / 32)
    repeat_factor = min(1.0, repeat_count / max(1, int(len(chords) * 0.4)))
    form_bonus = 0.15 * length_factor * repeat_factor

    # Cadence bonus: reward smoother adjacent motion on the circle.
    adjacent_distances = [
        get_circle_of_fifths_distance(chords[i], chords[i + 1])
        for i in range(len(chords) - 1)
    ]
    avg_adjacent_distance = (
        sum(adjacent_distances) / len(adjacent_distances)
        if adjacent_distances
        else 6.0
    )
    cadence_bonus = 0.12 * max(0.0, 1.0 - (avg_adjacent_distance / 6.0))

    return min(1.0, score + form_bonus + cadence_bonus)

if __name__ == "__main__":
    with open("testing/chords.txt", "r") as f:
        file = f.read()

    print(analyze_chords(file))

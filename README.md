# Music App

## Score Legend

### Final song score
- Range: `0.00` to `1.00`
- Formula: `0.70 * chord_score + 0.30 * lyric_score`
- Lyrics floor: lyric score is clamped to a minimum of `0.45` before final mixing

### Chord score
- Base range: `0.00` to `1.00`
- Final range: includes up to `+0.15` form bonus and up to `+0.12` cadence bonus, then capped at `1.00`
- Weights:
  - `15%` unique chord ratio (repeat-tolerant)
  - `50%` chord complexity (extensions and symbols)
  - `35%` harmonic structure (circle-of-fifths distance pattern)
- Extra bonus:
  - Cadence bonus rewards smoother adjacent chord motion on the circle of fifths

### Lyric score
- Range: `0.00` to `1.00`
- Weights:
  - `40%` lexical diversity (type-token ratio)
  - `30%` average sentence length (normalized to `20`)
  - `30%` syntactic depth (normalized to `10`)

### Interpretation bands
- `0.00` to `0.39`: low
- `0.40` to `0.59`: fair
- `0.60` to `0.74`: good
- `0.75` to `0.89`: strong
- `0.90` to `1.00`: excellent

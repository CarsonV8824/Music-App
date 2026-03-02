import pandas as pd

from services.machine_learning import get_score_of_lyrics_from_model

from services.improved_song_lyrics import analyze_lyrics

import seaborn as sns
import matplotlib.pyplot as plt

df = pd.read_csv("song lyrics/billboard_top_100.csv")
lyrics:list[str] = df["Lyrics"].to_list()
years:list[str] = df["Hot100 Ranking Year"].to_list()
print(len(lyrics), len(years))
new_lyrics = []
new_years = []

for i, lyric in enumerate(lyrics):
    try:
        new_lyric = lyric.replace("[", "").replace("]", "").replace("'", "").replace(", ", " ")
        new_lyrics.append(new_lyric)
        new_years.append(years[i])
    except Exception as e:
        print(f"error adding line: {e}")
print(f"{len(new_lyrics)} out of {len(lyrics)} were used.")

year_and_text_data = zip(new_years, new_lyrics)

rows = []

for year, text in year_and_text_data:   # <-- FIXED ORDER
    try:
        score = get_score_of_lyrics_from_model(text)
        rows.append({
            "text": text,
            "year": year,
            "score": score
        })
    except Exception:
        continue
print("so close")
print(len(rows))
df = pd.DataFrame(rows)

ax = sns.boxplot(data=df, x="year", y="score")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
ax.set_title("Billboard top 100 songs Every Year and the Lyrical Complexity of thier Songs")
plt.tight_layout()
plt.show()

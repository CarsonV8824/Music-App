from sklearn.linear_model import LinearRegression
import numpy as np
import joblib
import pandas as pd
import sys

from improved_song_lyrics import analyze_lyrics

df = pd.read_csv("song lyrics/billboard_top_100.csv")
lyrics:list[str] = df["Lyrics"].to_list()
new_lyrics = []
for lyric in lyrics:
    try:
        new_lyric = lyric.replace("[", "").replace("]", "").replace("'", "").replace(", ", " ")
        new_lyrics.append(new_lyric)
    except Exception as e:
        print(f"error adding line: {e}")
print(f"{len(new_lyrics)} out of {len(lyrics)} were used.")

data = []
for i, lyric in enumerate(new_lyrics):
    try:
        result = analyze_lyrics(lyric)
        if len(result) == 10:
            print(f"Index {i}: result length = {len(result)}")
            data.append(result)
    except Exception as e:
        print(f"Error at index {i}: {e}")
        print(f"Lyric: {lyric[:100]}")
        break

model = LinearRegression()

X = np.array(data, dtype=object)  # or handle padding manually
y = np.array([line[0] for line in data])
model.fit(X, y)

predictions = model.predict([analyze_lyrics("help me like the sun")])

print(predictions)

# save model
filename = "lyric_model.joblib"

joblib.dump(model, filename)

# load model
loaded_model:LinearRegression = joblib.load(filename)


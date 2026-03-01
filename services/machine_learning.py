from sklearn.linear_model import LinearRegression
import numpy as np
import joblib
import pandas as pd
import sys

from improved_song_lyrics import analyze_lyrics

df = pd.read_csv("song lyrics/billboard_top_100.csv")
lyrics:list[str] = df["Lyrics"].head(1000).to_list()
new_lyrics = []
for lyric in lyrics:
    try:
        new_lyric = lyric.replace("[", "").replace("]", "").replace("'", "").replace(", ", " ")
        new_lyrics.append(new_lyric)
    except Exception as e:
        print(f"error adding line: {e}")
print(f"{len(new_lyrics)} out of {len(lyrics)} were used.")

data = []
for lyric in new_lyrics:
    data.append(analyze_lyrics(lyric))

model = LinearRegression()

X = np.array(data)
y = np.array([line[0] for line in data])
model.fit(X, y)

predictions = model.predict([analyze_lyrics("help me like the sun")])

print(predictions)

# save model
filename = "lyric_model.joblib"

joblib.dump(model, filename)

# load model
loaded_model:LinearRegression = joblib.load(filename)


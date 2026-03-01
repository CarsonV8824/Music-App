from sklearn.linear_model import LinearRegression
import numpy as np

import joblib

model = LinearRegression()

X = np.array([[1], [2], [3], [4]])  # 2D array (4x1)
y = np.array([2, 4, 6, 8])
model.fit(X, y)

predictions = model.predict([[5]])

print(predictions)

# save model
filename = "my_model.joblib"

joblib.dump(model, filename)

# load model
loaded_model:LinearRegression = joblib.load(filename)

load_pred = loaded_model.predict([[7]])

print(load_pred)
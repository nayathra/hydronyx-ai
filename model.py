from sklearn.ensemble import RandomForestClassifier
import numpy as np

model = RandomForestClassifier()

X = [
    [30, 0, 50],
    [60, 1, 70],
    [80, 1, 90],
    [40, 0, 60]
]

y = ["LOW", "MEDIUM", "HIGH", "LOW"]

model.fit(X, y)


def predict_risk(water, rain, humidity):
    prediction = model.predict([[water, rain, humidity]])
    return prediction[0]
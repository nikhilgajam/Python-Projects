import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle
import pickle
import time

data = pd.read_csv("student-mat.csv", sep=";")
data = data[['G1', 'G2', 'G3', 'studytime', 'absences', 'health']]

predict = "G3"

X = np.array(data.drop([predict], 1))
y = np.array(data[[predict]])

best_accuracy = 0

start_time = time.time()

print("Working on it...")

for i in range(10000):

    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.1)

    linear = linear_model.LinearRegression()

    linear.fit(x_train, y_train)
    accuracy = linear.score(x_test, y_test)*100

    if accuracy > best_accuracy:
        best_accuracy = accuracy
        with open("BestStudentModel", "wb") as p:
            pickle.dump(linear, p)

end_time = time.time()
time_taken = end_time-start_time

print("Best Accuracy:", best_accuracy)
print("Time Taken: ", time_taken, "seconds")

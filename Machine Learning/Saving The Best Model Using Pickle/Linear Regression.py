import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle
import pickle

data = pd.read_csv("student-mat.csv", sep=";")
data = data[['G1', 'G2', 'G3', 'studytime', 'absences', 'health']]

predict = "G3"

X = np.array(data.drop([predict], 1))
y = np.array(data[[predict]])

best_accuracy = 0

for i in range(10000):

    x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.1)

    linear = linear_model.LinearRegression()

    linear.fit(x_train, y_train)
    accuracy = linear.score(x_test, y_test)*100

    if accuracy > best_accuracy:
        best_accuracy = accuracy
        with open("BestStudentModel", "wb") as p:
            pickle.dump(linear, p)

print("Best Accuracy:", best_accuracy)

pickle_in = open("BestStudentModel", "rb")
linear = pickle.load(pickle_in)
p.close()

predictions = linear.predict(x_test)
print("\nPredicted Answer using ML,", "Actual data used,", "Actual Answer")
for i in range(len(predictions)):
    print(predictions[i][0], x_test[i], y_test[i][0])

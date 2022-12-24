import pandas as pd
import numpy as np
import sklearn
from sklearn import linear_model
from sklearn.utils import shuffle
from matplotlib import pyplot as plt
from matplotlib import style

data = pd.read_csv("student-mat.csv", sep=";")
data = data[['G1', 'G2', 'G3', 'studytime', 'absences', 'health']]

predict = "G3"

X = np.array(data.drop([predict], 1))
y = np.array(data[[predict]])

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.1)

linear = linear_model.LinearRegression()

linear.fit(x_train, y_train)
accuracy = linear.score(x_test, y_test)
print("Accuracy:", round(accuracy*100, 2))

predictions = linear.predict(x_test)
print("\nPredicted Answer using ML,", "Actual data used,", "Actual Answer")
for i in range(len(predictions)):
    print(predictions[i][0], x_test[i], y_test[i][0])

# Giving other data to predict the answer
predictions = linear.predict([[13, 14, 3, 6, 2], ])
print("\nPredicted value:", predictions[0])

# Plotting
p = 'G1'  # You can use other column names
style.use('ggplot')
plt.scatter(data[[p]], data[['G3']])
plt.xlabel(p)
print(p)
plt.ylabel('Prediction')
plt.show()

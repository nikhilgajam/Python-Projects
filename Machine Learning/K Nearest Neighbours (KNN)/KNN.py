import sklearn
from sklearn.utils import shuffle
from sklearn.neighbors import KNeighborsClassifier
import pandas as pd
import numpy as np
from sklearn import linear_model, preprocessing

data = pd.read_csv("car.data")

# Converting the non numeric data into numeric
le = preprocessing.LabelEncoder()
buying = le.fit_transform(list(data['buying']))
maint = le.fit_transform(list(data['maint']))
doors = le.fit_transform(list(data['doors']))
persons = le.fit_transform(list(data['persons']))
lug_boot = le.fit_transform(list(data['lug_boot']))
safety = le.fit_transform(list(data['safety']))
cls = le.fit_transform(list(data['class']))


# Model

predict = 'class'

X = list(zip(buying, maint, doors, persons, lug_boot, safety))
y = list(cls)

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(X, y, test_size=0.1)

model = KNeighborsClassifier(n_neighbors=5)

model.fit(x_train, y_train)
accuracy = model.score(x_test, y_test)
print(accuracy)

predicted = model.predict(x_test)

names = ["unacc", "acc", "good", "vgood"]

for i in range(len(predicted)):
    print("Predicted:", names[predicted[i]], ", Data:", x_test[i], ", Actual:", names[y_test[i]])

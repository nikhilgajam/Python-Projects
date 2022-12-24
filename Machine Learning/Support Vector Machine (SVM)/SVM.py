import sklearn
from sklearn import datasets
from sklearn import svm
from sklearn import metrics

# Using sklearn inbuilt dataset
data = datasets.load_breast_cancer()

# print(data.feature_names)
# print(data.target_names)

# Using data
x = data.data
y = data.target

x_train, x_test, y_train, y_test = sklearn.model_selection.train_test_split(x, y, test_size=0.2)
classes = ['malignant', 'benign']

# Creating and training the model      website: https://scikit-learn.org/stable/modules/generated/sklearn.svm.SVC.html
classifier = svm.SVC(kernel="linear")   # kernel = linear | poly | rbf | sigmoid, degree = 3 (default), C = 1.0(default soft margin)
classifier.fit(x_train, y_train)

y_pred = classifier.predict(x_test)

# Accuracy evalutation
accuracy = metrics.accuracy_score(y_test, y_pred)

print("Accuracy:", accuracy*100)

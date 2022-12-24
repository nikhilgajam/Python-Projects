import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix
from sklearn.model_selection import train_test_split
from sklearn.metrics import recall_score, precision_recall_fscore_support, roc_curve
import matplotlib.pyplot as plt

sensitivity_score = recall_score
def specificity_score(y_true, y_pred):
    p, r, f, s = precision_recall_fscore_support(y_true, y_pred)
    return r[0]

# Reading
df = pd.read_csv("titanic.csv")
df['male'] = df['Sex'] == 'male'   # Going to create a new column with male values to True

X = df.loc[:, ~df.columns.isin(["Survived", "Sex"])].values  # Selecting all columns except some
y = df["Survived"].values

model = LogisticRegression()
model.fit(X, y)

print(model.predict([[3, True, 22.0, 1, 0, 7.25]]))  # Predicting single value
print(model.predict([X[0]]))  # Single value also needs 2D array
print(model.predict(X[:5]))  # Predicting multiple values
print(y[:5])

# Scoring the model
y_pred = model.predict(X)
score = (y_pred == y).sum() / y.shape[0]  # Correctly predicted / total no of values
print(score)

print(model.score(X, y))  # Inbuilt method to score

# Metrics
print(accuracy_score(y, y_pred))
print(precision_score(y, y_pred))
print(recall_score(y, y_pred))
print(f1_score(y, y_pred))
print(confusion_matrix(y, y_pred))

# Sklearn splits training and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=10)

print("whole dataset:", X.shape, y.shape)
print("training set:", X_train.shape, y_train.shape)
print("test set:", X_test.shape, y_test.shape)

# Sensitivity and specificity
y_pred = model.predict(X_test)

print("sensitivity:", sensitivity_score(y_test, y_pred))
print("specificity:", specificity_score(y_test, y_pred))

# Adjusting the Logistic Regression Threshold in Sklearn
y_pred = model.predict_proba(X_test)[:, 1] > 0.75

print("precision:", precision_score(y_test, y_pred))
print("recall:", recall_score(y_test, y_pred))

# ROC curve
y_pred_proba = model.predict_proba(X_test)
fpr, tpr, thresholds = roc_curve(y_test, y_pred_proba[:,1])

plt.plot(fpr, tpr)
plt.plot([0, 1], [0, 1], linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.xlabel('1 - specificity')
plt.ylabel('sensitivity')
plt.show()

# Area Under the Curve (AUC)
model1 = LogisticRegression()
model1.fit(X_train, y_train)
y_pred_proba1 = model1.predict_proba(X_test)
print("model 1 AUC score:", roc_auc_score(y_test, y_pred_proba1[:, 1]))

model2 = LogisticRegression()
model2.fit(X_train[:, 0:2], y_train)
y_pred_proba2 = model2.predict_proba(X_test[:, 0:2])
print("model 1 AUC score:", roc_auc_score(y_test, y_pred_proba2[:, 1]))
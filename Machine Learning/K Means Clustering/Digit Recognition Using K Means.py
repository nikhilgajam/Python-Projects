# Importing libraries
import matplotlib.pyplot as plt
from tkinter import *
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import random


def run():
    # Loading the data
    digits_dataset = datasets.load_digits()

    # Feature allocation
    sample_features = digits_dataset.data
    labels = digits_dataset.target

    # Splitting the data for training and testing sets
    rs = random.randint(1, 101)
    train_img, test_img, train_lbl, test_lbl = train_test_split(sample_features, labels, test_size=0.2, random_state=rs)

    # Fit the algorithm
    Knn = KNeighborsClassifier(n_neighbors=7)
    Knn.fit(train_img, train_lbl)

    # Predict the data
    ans = Knn.predict(test_img[[0]])
    display.insert(INSERT, "Predicted data: " + str(ans[0]) + "\n")

    # Accuracy
    display.insert(INSERT, "Accuracy of this model:" + str(Knn.score(test_img, test_lbl)*100) + "\n")
    display.insert(INSERT, "Displaying the predicted image in dataset:\n\n\n")
    

    # Seeing the data in the dataset
    plt.imshow(digits_dataset.images[ans[0]], cmap=plt.cm.gray_r, interpolation="nearest")
    plt.show()


root = Tk()
root.title("Digit Recognition")

label = Label(root, text="Digit Recognition", font=("Times New Roman", 26))
label.pack()

display = Text(root)
display.pack()

rndm_btn = Button(root, text="Predict", command=run)
rndm_btn.pack()

root.mainloop()

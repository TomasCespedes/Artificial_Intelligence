# Author: Tomas Cespedes
# Purpose: Data analytics
# Citations:
# Collaboration: Worked with Taylor Digilio

from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import cross_val_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn import tree
import numpy as np
import matplotlib.pyplot as plt

breast_cancer = load_breast_cancer()
x = breast_cancer.data
y = breast_cancer.target

# How many examples are there?
print("Number of Examples: " + str(len(breast_cancer.data)))

# How many classes are there?
print("There are 2 classes within the data set breast_cancer.")

# What do the classes represent?
print("The classes represent whether the tumor is malignant (0) or benign(1).")

# How many examples of each class are there?
malignant_counter = 0
benign_counter = 0

# Go through data set to count
for i in range(len(breast_cancer.target)):
    if breast_cancer.target[i] == 1:
        benign_counter += 1
    else:
        malignant_counter += 1

# Print out the number of cases
print("Number of malignant cases: " + str(malignant_counter))
print("Number of benign cases: " + str(benign_counter))

# How many features are there?
print("There are " + str(len(breast_cancer.feature_names)) + " features in this data set.")

# What data type are the features?
print("The data types of the features are " + str(x.dtype), "\n")

# Make a train/test split of this dataset to use for classification.
# Write some code to confirm that it balances classes reasonably.
train = np.arange(0, len(y), 2)
test = np.arange(1, len(y), 2)
print("Total Train Set length:", len(train))
print("Total Test Set length:", len(test))

y_train = y[train]
y_test = y[test]

# Count the number of cases we see in train set
benign_counter = 0
for i in y_train:
    if i == 1:
        benign_counter += 1

# Count the number of cases we see in test set
benign_counter_test = 0
for i in y_test:
    if i == 1:
        benign_counter_test += 1

# Print out the results
print("Number of Benign cases in Training Set:", benign_counter)
print("Number of Benign cases in Testing Set: " + str(benign_counter_test))
print("As we can see from the data above, this is a fairly good split. \n")

# Decision Tree Classifier
clf = DecisionTreeClassifier()
clf.fit(x[train], y[train])
print("Cross Validation Decision Tree Scores: ", cross_val_score(clf, x[test], y[test], cv=3))

# Run your program a few times and note that the score changes slightly.
# Look in the documentation to discover why this is happening.
# Print a quick explanation here.
print("The decision tree classifier has a random_state which is the seed used by the random number generator."
      " \n If we do not specify the seed, then it will randomly choose a seed for us."
      " \n As a result, every time we run it a different seed is chosen which will give us different numbers everytime.")

# The main setting to consider for a decision tree is how deep to make it.
# One way to control this in the sklearn decision tree is the min_samples_leaf parameter.
# What is the default setting for this parameter?
# Print your answer here.
print("The default for the min_samples_leaf parameter is 1.")

# Generate a plot to show how this parameter affects the score of your classifier.
# Try 1 through 15 and plot them on the x-axis, with the corresponding scores on the y-axis.
for i in range(16):
    if i == 0:
        pass
    else:
        clf = DecisionTreeClassifier(min_samples_leaf=i, random_state=1)
        clf.fit(x[train], y[train])
        plt.scatter(i, clf.score(x[test], y[test]))

# Label the figure and its axes
plt.title("Decision Tree Classifier")
plt.xlabel("Min sample Leaf value")
plt.ylabel("Corresponding Scores")
plt.show()
plt.clf()

# Print the best setting, along with the score that it achieves.
print("The best settings are when the min_samples_leaf equals either 10 or 11 with a score of 0.9190.\n")

# Look up the export_graphviz function and use it to save your best decision tree to a file.
# Copy and paste it into http://www.webgraphviz.com/ to see what it looks like.
# Take a screenshot so that you can submit an image of the tree.
clf = DecisionTreeClassifier(min_samples_leaf=10, random_state=1)
clf = clf.fit(x[train], y[train])
tree.export_graphviz(clf, out_file="treecode")


# Look up the sklearn nearest-neighbor classifier.
# Fit one to your train data, and print its score on your test data.
clf = KNeighborsClassifier()
clf.fit(x[train], y[train])
print("K-Nearest Neighsbors score:", clf.score(x[test], y[test]))

# There are several important settings to consider for nearest-neighbor classifiers.
# One of them is the distance metric that we use to calculate who is nearest.
# Given the data type of the features you're working with, what metric makes sense to use?
# And according to the documentation, what metric is being used by default?
# Print your answers here.
print("The default value for K-Nearest neighbors is set to 5.")
print("I believe that the best metric to use would be the default of 5 but not with the distance weight.")
print("It not only gives us the best score but it is a good median number where it checks those around it but not too few or too many.")

# Two other important settings are the number of neighbors to use and whether or not to weight them by distance.
# What are the default settings for these in sklearn?
# Print your answers here.
print("The default setting of the weights is uniform. That means all the points are weighted equally.")


# Generate a plot to show how these parameters affects the score of your classifier.
# Plot two curves (one with distance weighting, one without) and include a legend to show which is which.
clf_scores = list()
clfd_scores = list()
selections = [1, 3, 5, 7, 9]

# Go through all the selections
for i in selections:
    # Use K-Nearest Neighbors
    clf = KNeighborsClassifier(n_neighbors=i)
    # Use K-nearest Neighbors with weights as distance
    clfd = KNeighborsClassifier(n_neighbors=i, weights='distance')
    # Fit the model to data
    clf.fit(x[train], y[train])
    clfd.fit(x[train],y[train])
    # Get the score
    score = clf.score(x[test], y[test])
    scored = clfd.score(x[test], y[test])
    # Add the score to list
    clf_scores.append(score)
    clfd_scores.append(scored)

# Plot our scores
plt.plot(selections, clf_scores)
plt.plot(selections, clfd_scores)

# Label the figure and its axes
plt.title("Nearest Neighbor Classifier")
plt.xlabel("Number of Neighbors")
plt.ylabel("Corresponding Scores")

# Show the plot
plt.show()
plt.clf()

# Print the best settings, along with the score that they achieve.
print("As we guessed correctly, the classifier with k = 5 nearest neighbors had the best score of 0.92958 when we weighted all points equally.\n")
print("However, when we set the weights to distance, we see k = 7 have the best score of 0.923. This is worse than using the uniform weights though.")


# Based on your results, which classifier is more effective for breast cancer diagnosis?
print("In terms of scores and consistency, I believe K-nearest neighbors was most effective. It had the highest score of 0.92958.")
print("However, the decision tree had a score of 0.9190 in it's best state so it was not too far off from K-nearest Neighbors.")

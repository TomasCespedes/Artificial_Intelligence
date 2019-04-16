# Author: Tomas Cespedes
# Purpose: Run different pipelines on Sklearn: Wine dataset
# Citations: Classifier documentation on Sklearn.
from sklearn.datasets import load_wine
from sklearn.feature_selection import SelectKBest
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
import numpy as np
import matplotlib.pyplot as plt

# Load the wine data set
wine = load_wine()
x = wine.data
y = wine.target

# Pipeline for SVC
pipe_SVC = Pipeline([
    # Tell pipeline which methods to use
    ('scale', StandardScaler()),
    ('select', SelectKBest()),
    ('classify', SVC(kernel='linear'))
])

# Hyperparameters we want to try
settings = {
    'scale__with_mean': [False, True],
    'scale__with_std': [False, True],
    'select__k': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
    'classify__C': [0.1, 1, 10],
}

# Get an unbiased estimate of this pipeline score
grid_SVC = GridSearchCV(pipe_SVC, settings, cv=5, iid=False)
scores_SVC = cross_val_score(grid_SVC, x, y, cv=5)

# Print the scores of SVC
print("SVC Scores:", scores_SVC)
print("Mean:", scores_SVC.mean())
print("Std:", scores_SVC.std())
# Printing the best settings to use in this pipeline
grid_SVC.fit(x, y)
print("Best settings:", grid_SVC.best_params_)

# Pipeline for Decision Tree Classifier
pipe_DTC = Pipeline([
    ('scale', StandardScaler()),
    ('select', SelectKBest()),
    ('classify', DecisionTreeClassifier(random_state=1))
])

# Hyperparameters we want to try
settings = {
     'scale__with_mean': [False, True],
     'scale__with_std': [False, True],
     'select__k': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
     'classify__min_samples_leaf': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15],
}

# Get an unbiased estimate of this pipeline score
grid_DTC = GridSearchCV(pipe_DTC, settings, cv=5, iid=False)
scores_DTC = cross_val_score(grid_DTC, x, y, cv=5)

# Print the scores for decision trees
print("Decision Tree Scores:", scores_DTC)
print("Mean:", scores_DTC.mean())
print("Std:", scores_DTC.std())

# Printing the best settings to use in this pipeline
grid_DTC.fit(x, y)
print("Best settings:", grid_DTC.best_params_)

# Pipeline for K-Nearest Neighbors Classifier
pipe_KNC = Pipeline([
    ('scale', StandardScaler()),
    ('select', SelectKBest()),
    ('classify', KNeighborsClassifier())
])

# Hyperparameters we want to try
settings = {
    'scale__with_mean': [False, True],
    'scale__with_std': [False, True],
    'select__k': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
    'classify__n_neighbors': [1, 2, 3, 5, 7, 9],
    'classify__weights': ['distance', 'uniform'],
}

# Get an unbiased estimate of this pipeline score
grid_KNC = GridSearchCV(pipe_KNC, settings, cv=5, iid=False)
scores_KNC = cross_val_score(grid_KNC, x, y, cv=5)

# Print the scores for K-Nearest Neighbors
print("K-Nearest Neighbors Score:", scores_KNC)
print("Mean:", scores_KNC.mean())
print("Std:", scores_KNC.std())

# Printing the best settings to use in this pipeline
grid_KNC.fit(x, y)
print("Best settings:", grid_KNC.best_params_)

# Pipeline for GaussianNB
pipe_GNB = Pipeline([
    ('scale', StandardScaler()),
    ('select', SelectKBest()),
    ('classify', GaussianNB())
])

# Hyperparameters we want to try
settings = {
    'scale__with_mean': [False, True],
    'scale__with_std': [False, True],
    'select__k': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13],
    }

# Get an unbiased estimate of this pipeline score
grid_GNB = GridSearchCV(pipe_GNB, settings, cv=5, iid=False)
scores_GNB = cross_val_score(grid_GNB, x, y, cv=5)

# Print the scores for Gaussian Naive Bayes
print("Gaussian Naive Bayes Score:", scores_GNB)
print("Mean:", scores_GNB.mean())
print("Std:", scores_GNB.std())

# Printing the best settings to use in this pipeline
grid_GNB.fit(x, y)
print("Best settings:", grid_GNB.best_params_)

# Group the classifiers for X-axis
classifiers = ["GNB", "DTC", "KNC", "SVC"]

# Get the number of X-indices
indices = np.arange(len(classifiers))

# Put mean scores for classifiers into an array
mean_scores = [scores_SVC.mean(), scores_DTC.mean(), scores_KNC.mean(), scores_SVC.mean()]

# Put standard deviation scores for classifiers into an array
std_scores = [scores_SVC.std(), scores_DTC.std(), scores_KNC.std(), scores_SVC.std()]

# Plot it as a bar graph
plt.bar(indices, mean_scores, yerr=std_scores, align='center', bottom=None, alpha=0.5)
plt.xticks(indices, classifiers)
plt.title("Means of Classifiers")
plt.xlabel("Classifiers")
plt.ylabel("Classifier Means")
plt.show()


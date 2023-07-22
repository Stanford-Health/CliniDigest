from process_data import *
from evaluation import *
import numpy as np
import warnings
import re
import os
import pickle
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.metrics import precision_score, make_scorer
from sklearn.linear_model import LogisticRegression
from sklearn.utils import resample
import matplotlib.pyplot as plt
from scipy.spatial import distance
from sklearn.metrics import roc_curve, auc

def predict_initial(category, best_model, X_test, y_test):
    probabilities = best_model.predict_proba(X_test)[:, 1]

    fpr, tpr, thresholds = roc_curve(y_test, probabilities)
    roc_auc = auc(fpr, tpr)

    # Plot ROC curve (commented out for better performance)
    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (AUC = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(category)
    plt.legend(loc="lower right")
    plt.show(block=False)

    distances = distance.cdist(np.array([0, 1]).reshape(1, 2), np.column_stack((fpr, tpr)), 'euclidean')[0]

    # Find the index of the point with the smallest distance
    optimal_index = np.argmin(distances)

    

    optimal_threshold = thresholds[optimal_index]

    # For debugging optimal point, comment out while actual use
    # Get the optimal operating point coordinates
    optimal_fpr = fpr[optimal_index]
    optimal_tpr = tpr[optimal_index]
    print("Optimal operating point coordinates: FPR = {}, TPR = {}, threshold = {}".format(optimal_fpr, optimal_tpr, optimal_threshold))
    return probabilities, y_test, optimal_threshold

def upsample_data(input_vectors, labels):
    input_vectors = np.array(input_vectors)
    labels = np.array(labels)

    indices_label_0 = np.where(labels == 0)[0]
    indices_label_1 = np.where(labels == 1)[0]
    if len(indices_label_0) > len(indices_label_1):
      indices_label_1 = resample(indices_label_1, n_samples = len(indices_label_0), random_state=19)

    else:
      indices_label_0 = resample(indices_label_0, n_samples = len(indices_label_1), random_state=19)
    upsampled_indices = np.concatenate((indices_label_1, indices_label_0))
    upsampled_input_vectors = input_vectors[upsampled_indices]
    upsampled_labels = labels[upsampled_indices]

    return upsampled_input_vectors, upsampled_labels

def train_model(X_train, y_train):

    scorer = make_scorer(precision_score)

    param_grid = {'C': [0.001, 0.01, 0.1, 1, 10, 100, 1000, 10000],
                  'penalty': ['l1', 'l2'],
                 }
    model = LogisticRegression(multi_class="auto", solver="liblinear", class_weight='balanced')
    grid_search = GridSearchCV(model, param_grid, scoring=scorer)
    grid_search.fit(X_train, y_train)
    best_model = grid_search.best_estimator_

    best_model.fit(X_train, y_train)
    return best_model
    
def train(vectorize_type):
    # converts csv into array of processed strings
    csv_file_path = 'data/fitbit_input.csv'
    column_dict = read_csv_to_dict(csv_file_path)
    string_inputs = [column_dict["Title"][i] + column_dict["Description"][i] for i in range(len(column_dict["Description"]))]
    input_vectors = string_to_vector(vectorize_type, string_inputs)

    # Note: Gastroenterolgy and Other is omitted here
    medical_fields = ["Somnology", "Gynecology", "Obstetrics", "Cardiology", "General Physiology", "Endocrinology", "Bariatrics", "Psychiatry", "Oncology", "Pulmonology", "Chronic pain / diseases"]#, "Other"]

    # change to 0, when actually runnning it
    test_proportion = 0.3
    top_three_categories = [[(-1, "")] * 3 for _ in range(int(test_proportion * len(column_dict["Title"])+1))]

    # loops through all medical fields and populates actual_labels and top_three_categories, which are the
    # top 3 categories with the most probability for each clinical trial (an element is a tuple: (probability, category))
    actual_labels = [[] for _ in range(int(test_proportion * len(column_dict["Title"])+1))]
    optimal_thresholds = []
    for medical_field in medical_fields:
        labels = [1 if
            column_dict["Primary Category"][i] == medical_field or
            column_dict["Secondary Category"][i] == medical_field or
            column_dict["Tertiary Category"][i] == medical_field
            else 0
            for i in range(len(column_dict["Primary Category"]))]

        X_train, X_test, y_train, y_test = train_test_split(input_vectors, labels, test_size=test_proportion, shuffle=20)
        X_train, y_train = upsample_data(X_train, y_train)
        best_model = train_model(X_train, y_train)
        folder_name = 'LogisticClassifier/model_' + vectorize_type
        if not os.path.exists(folder_name):
            os.makedirs(folder_name)
        medical_field_filename = re.sub(r"[^\w\s]", '-', medical_field)
        filename = os.path.join(folder_name, 'model_' + medical_field_filename)
        pickle.dump(best_model, open(filename, 'wb'))
        probabilities, y_test, optimal_threshold = predict_initial(medical_field, best_model, X_test, y_test)
        optimal_thresholds.append(optimal_threshold)

        predicted_labels = [1 if i >= optimal_threshold else 0 for i in probabilities]
        #comment out for performance / ease of understanding log
        calculate_metrics_one_field(y_test, predicted_labels, medical_field)

        for i in range(len(probabilities)):
            if y_test[i] == 1:
                actual_labels[i].append(medical_field)
            min_tuple = min(top_three_categories[i], key=lambda x: x[0])
            min_tuple_index = top_three_categories[i].index(min_tuple)
            if probabilities[i] > min_tuple[0] and probabilities[i] >= optimal_threshold:
                top_three_categories[i][min_tuple_index] = (probabilities[i], medical_field)

    # extracts just the categories from top_three_categories
    predicted_labels = []
    for row in top_three_categories:
        row_strings = [element[1] for element in row]
        predicted_labels.append(row_strings)
    np.save('LogisticClassifier/optimal_thresholds.npy', optimal_thresholds)

    calculate_metrics(actual_labels, predicted_labels, vectorize_type)
  
warnings.filterwarnings('ignore')
print(" -----------------------------")
print("|     Metrics using TF-IDF    |")
print(" -----------------------------")
train("tfidf")
print("================================")
print(" -----------------------------")
print("|      Metrics using BoW      |")
print(" -----------------------------")
train("bow")
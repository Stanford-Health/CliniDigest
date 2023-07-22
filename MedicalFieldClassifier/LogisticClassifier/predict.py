from process_data import *
from evaluation import *
import numpy as np
import os
import pickle

def predict(vectorize_type, csv_file_path):
    # process data
    column_dict = read_csv_to_dict(csv_file_path)
    string_inputs = [column_dict["Title"][i] + column_dict["Description"][i] for i in range(len(column_dict["Description"]))]
    processed_clinical_trial_descriptions = string_to_vector(vectorize_type, string_inputs)
    # Note: Gastroenterolgy and Other is omitted here
    medical_fields = ["Somnology", "Gynecology", "Obstetrics", "Cardiology", "General Physiology", "Endocrinology", "Bariatrics", "Psychiatry", "Oncology", "Pulmonology", "Chronic pain / diseases"]#, "Other"]
    optimal_thresholds = np.load('LogisticClassifier/optimal_thresholds.npy').tolist()
    top_three_categories = [[(-1, "")] * 3 for _ in range(len(processed_clinical_trial_descriptions))]
    for medical_field_i in range(len(medical_fields)):
        medical_field_filename = re.sub(r"[^\w\s]", '-', medical_fields[medical_field_i])

        for filename in os.listdir('LogisticClassifier/model_' + vectorize_type):
            if filename == 'model_' + medical_field_filename:
                filepath = os.path.join('LogisticClassifier/model_' + vectorize_type, filename)
                with open(filepath, 'rb') as file:
                    best_model = pickle.load(file)
        probabilities = best_model.predict_proba(processed_clinical_trial_descriptions)[:, 1]
        for i in range(len(probabilities)):
            min_tuple = min(top_three_categories[i], key=lambda x: x[0])
            min_tuple_index = top_three_categories[i].index(min_tuple)
            if probabilities[i] > min_tuple[0] and probabilities[i] >= optimal_thresholds[medical_field_i]:
                top_three_categories[i][min_tuple_index] = (probabilities[i], medical_fields[medical_field_i])

    # extracts just the categories from top_three_categories
    predicted_labels = []
    for row in top_three_categories:
        row_strings = [element[1] for element in row]
        predicted_labels.append(row_strings)
    np.save('LogisticClassifier/predictions_' + vectorize_type + '.npy', predicted_labels)
  
csv_file_path = 'data/fitbit_input.csv'
predict("tfidf", csv_file_path)
predict("bow", csv_file_path)
# print(np.load('predictions_tfidf.npy').tolist())
# print(np.load('predictions_bow.npy').tolist())
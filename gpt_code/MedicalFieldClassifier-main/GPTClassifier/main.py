from process_data import *
from evaluation import *
from predict import *
import numpy as np

clinical_trials = read_csv_to_dict(r"C:\Users\jimdw\OneDrive-Stanford\Documents\Research\Classifier\GPTClassifier\DevicesCompletedTrialsToAdd.csv")
clinical_trials_descriptions = clinical_trials["Description"]

predicted_labels = predict(clinical_trials_descriptions)

filename = 'GPTClassifier/GPT_predictions.txt'
with open(filename, 'w') as f:
    f.writelines('\n'.join(predicted_labels))

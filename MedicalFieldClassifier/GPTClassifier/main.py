from process_data import *
from evaluation import *
from predict import *
import numpy as np

clinical_trials = read_csv_to_dict('data/fitbit_input.csv')
clinical_trials_descriptions = clinical_trials["Description"]

predicted_labels = predict(clinical_trials_descriptions)

filename = 'GPTClassifier/GPT_predictions.npy'
np.save(filename, predicted_labels)

# Comment out
actual_labels = get_actual_labels(clinical_trials)
calculate_metrics(actual_labels, predicted_labels)

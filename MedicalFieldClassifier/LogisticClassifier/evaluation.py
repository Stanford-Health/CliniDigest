import numpy as np


def calculate_metrics_one_field(actual, predicted, medical_field):
    # Counting True Positives, True Negatives, False Positives, and False Negatives
    tp = tn = fp = fn = 0

    for i in range(len(actual)):
        if actual[i] == 1 and predicted[i] == 1:
            tp += 1
        elif actual[i] == 0 and predicted[i] == 0:
            tn += 1
        elif actual[i] == 0 and predicted[i] == 1:
            fp += 1
        elif actual[i] == 1 and predicted[i] == 0:
            fn += 1

    # Calculate metrics
    if tp + fn == 0:
        tpr = "tp + fn == 0"
    else:
        tpr = tp / (tp + fn)

    if tn + fp == 0:
        tnr = "tn + fp == 0"
    else:
        tnr = tn / (tn + fp)

    if tp + fp == 0:
        ppv = "tp + fp == 0"
    else:
        ppv = tp / (tp + fp)

    if tp + tn + fp + fn == 0:
        accuracy = "(tp + tn) / (tp + tn + fp + fn)"
    else:
        accuracy = (tp + tn) / (tp + tn + fp + fn)

    if fp + tn == 0:
        fpr = "fp + tn == 0"
    else:
        fpr = fp / (fp + tn)
    # Return the calculated metrics
    print("==============================")
    print(medical_field)
    print("True Positive Rate (TPR):", tpr)
    print("False Positive Rate (FPR):", fpr)
    print("True Negative Rate (TNR):", tnr)
    print("Positive Predictive Value (PPV):", ppv)
    print("Accuracy:", accuracy)


def calculate_metrics(actual_labels, predicted_labels, vectorize_type):
    true_positives = 0
    true_negatives = 0
    false_positives = 0
    false_negatives = 0

    # Note: Gastroenterolgy and Other is omitted here
    medical_fields = ["Somnology", "Gynecology", "Obstetrics", "Cardiology", "General Physiology", "Endocrinology",
                      "Bariatrics", "Psychiatry", "Oncology", "Pulmonology", "Chronic pain / diseases"]  # , "Other"]

    for actual, predicted in zip(actual_labels, predicted_labels):
        for medical_field in medical_fields:
            if medical_field in predicted:
                if medical_field in actual:
                    true_positives += 1
                else:
                    false_positives += 1
            else:
                if medical_field in actual:
                    false_negatives += 1
                else:
                    true_negatives += 1

    if true_positives + false_negatives == 0:
        tpr = "No TPR"
    else:
        tpr = true_positives / (true_positives + false_negatives)

    if true_negatives + false_positives == 0:
        tnr = "No TNR"
    else:
        tnr = true_negatives / (true_negatives + false_positives)

    if true_positives + false_positives == 0:
        ppv = "No PPV"
    else:
        ppv = true_positives / (true_positives + false_positives)

    if true_positives + true_negatives + false_positives + false_negatives == 0:
        accuracy = "No accuracy"
    else:
        accuracy = (true_positives + true_negatives) / (true_positives +
                                                        true_negatives + false_positives + false_negatives)

    if false_positives + true_negatives == 0:
        fpr = "No FPR"
    else:
        fpr = false_positives / (false_positives + true_negatives)

    print("==== FINAL CLASSIFIER (for",vectorize_type,") ====")
    print("TPR:", tpr)
    print("FPR:", fpr)
    print("TNR:", tnr)
    print("PPV:", ppv)
    print("Accuracy:", accuracy)

    print("TP:", true_positives)
    print("FP:", false_positives)
    print("FN", false_negatives)
    print("TN", true_negatives)

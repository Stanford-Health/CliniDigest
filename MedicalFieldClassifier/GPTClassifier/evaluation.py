def get_actual_labels(clinical_trials):
    actual_labels = [[] for _ in range(len(clinical_trials["Description"]))]
    for i in range(len(clinical_trials["Primary Category"])):
        primary = clinical_trials["Primary Category"][i]
        actual_labels[i].append(primary)

        secondary = clinical_trials["Secondary Category"][i]
        if secondary is not None:
            actual_labels[i].append(secondary)

        tertiary = clinical_trials["Tertiary Category"][i]
        if tertiary is not None:
            actual_labels[i].append(tertiary)
    return actual_labels

def calculate_metrics(actual_labels, predicted_labels):
    true_positives = 0
    true_negatives = 0
    false_positives = 0
    false_negatives = 0

    #Note: Gastroenterolgy and Other is omitted here
    medical_fields = ["Somnology", "Gynecology", "Obstetrics", "Cardiology", "General Physiology", "Endocrinology", "Bariatrics", "Psychiatry", "Oncology", "Pulmonology", "Chronic pain / diseases"]#, "Other"]


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
        accuracy = (true_positives + true_negatives) / (true_positives + true_negatives + false_positives + false_negatives)
    print("TPR:", tpr)
    print("TNR:", tnr)
    print("PPV:", ppv)
    print("Accuracy:", accuracy)

    print("TP:", true_positives)
    print("FP:", false_positives)
    print("FN", false_negatives)
    print("TN", true_negatives)

# Medical Field Classifier

This repo consists of two classifiers that, given a list of clinical trials' titles and descriptions, can categorize each clinical trial into its primary, secondary, and ternary medical fields. The 11 medical fields referenced are Somnology, Gynecology, Obstetrics, Cardiology, General Physiology, Endocrinology, Bariatrics, Psychiatry, Oncology, Pulmonology, and Chronic pain / diseases (Note that "Gastroenterolgy" and "Other" are not present).

There are two classifiers included here:
- GPTClassifier
- LogisticClassifier



## 1. GPTClassifier
- The GPTClassifier is powered by GPT-3.5.
- The prompt given is: "Given the following classes of \"Somnology\", \"Gynecology\", \"Obstetrics\", \"Cardiology\", \"General Physiology\", \"Endocrinology\", \"Bariatrics\", \"Psychiatry\", \"Oncology\", \"Gastroenterology\", \"Pulmonology\", \"Chronic pain / diseases\", \"Other\" annotate one, two, or three classes for the following clinical trial. Note that a clinical trial doesn't necessarily need to have a secondary or tertiary medical field, but only one field should be in the primary, secondary, and tertiary fields", followed by a list of clinical trials' titles and descriptions.
- Usage:
    - Replace data/fitbit_input.csv to your csv file consisting of clinical trial data
    - Comment out lines 15-16 in GPTClassifier/main.py (since we do not have the actual medical fields)
    - Run GPTClassifier/main.py.
- It will save your predicted labels into GPTClassifier/GPT_predictions.npy

## 2. LogisticClassifier
- The LogisticClassifier is powered by sklearn's LogisticRegression.

- There are two main files of interest
    - train.py
    - predict.py
### 2.1 train.py
#### 2.1.1 Overview of train.py
- train.py trains the LogisticClassifier using the data found in ```data/fitbit_input.csv```. If you are training based on new or additional data, please make sure it is formatted in the same way as ```fitbit_input.csv```
- train.py trains the LogisticClassifier in two different ways, and outputs the metrics / evaluation for each:
    - Using TF-IDF
    - Using Bag of Words (BoW)
- train.py saves the trained model of each medical field for both TF-IDF and BoW methods. You can find them in the folders ```model_tfidf``` and ```model_bow```, respectively.
- NOTE: If you do not care about the evaluation metrics and want to maximize the training dataset, you can change test_proportion to 0 (on line 93).
#### 2.1.2 Detailed Walkthrough of train.py
It may be useful to read this side-by-side to ```train.py```
- The ```train()``` function first converts the csv file into an array of processed strings.
- top_three_categories is simply a data structure to keep track of the medical fields that is assigned the highest probability to each clinical trial. An element is a list of three tuples: 
    ```
    [(probability, category), (probability, category), (probability, category)]
    ```
    Each of the tuple, in no particular order, represents that clinical trial's primary, secondary, and tertiary category.
- It loops through each medical field and: 
    - populates actual_labels and top_three_categories. actual_labels is used for evaluation to compare with our predicted labels.
    - splits the input data into testing data and training
    - upsamples the training data for greater accuracy
    - trains the model based on training data
        - uses GridSearch to determine ideal C value and penalty (l1 or l2)
    - saves the model under ```LogisticClassifier/model_[tfidf or bow]/model_[medical field]```
    - determines the optimal threshold in ```predict_initial()``` for greater accuracy
    - saves the optimal threshold for the medical field model, which will be used in ```predictpy```
    - calculate and prints out the metrics for the classifier specific to that medical field
- Extract just the categories from top_three_categories, and call it predicted_labels
- Print out the final metrics for this classifier

### 2.2 predict.py
#### 2.2.1 Overview of predict.py
- ```predict.py``` is likely what you will use to predict new clinical trials' associated medical fields.
- ```predict.py``` predicts the medical fields of the clinical trials found in ```data/fitbit_input.csv```, so replace ```fitbit_input.csv``` with your data. Please make sure it is formatted in the same way as ```fitbit_input.csv```. You can leave the medical fields blank. This file only reads the clinical trials' title and description.
- It saves the predictions as a ```.npy``` file, which can be found in ```predictions_bow.npy``` and ```predictions_tfidf.npy```, based on which models it used (trained on Bag of Words, or TF-IDF).
- ```predict.py``` uses the models saved in ```train.py```
#### 2.2.2 Detailed Walkthrough of predict.py
It may be useful to read this side-by-side to ```predict.py```
- ```predict.py``` reads the new clinical trials in the ```.csv``` file and does some string processing.
- It loads the ```optimal_thresholds``` from the saved files (saved in ```train.py```).
- Like in ```predict.py```, ```top_three_categories``` is declared.
- It loops through the medical fields
    - It loads in each of the models associated with that medical field and method (BoW or TF-IDF)
    - It uses that model to predict the probabilities of each clinical trial being associated with that medical field.
    - Using those probabilities, it populates ```top_three_categories``` 
- Extract the categories from ```top_three_categories```, and call it ```predicted_labels```
- Save the predictions under ```LogisticClassifier/predictions_[tfidf or bow].npy```
    - Note that these predictions can then be converted to a list for your desired purpose with the following commands:
        ```
        np.load('predictions_tfidf.npy').tolist()
        np.load('predictions_bow.npy').tolist()
        ```
## Contributing
Contributions are very welcomed! Some future work include, but isn't limite to:
- Increasing PPV value
- Reorganizing code for easier use / workflow
- More training data through manual annotation of medical fields


## Author(s)
For support, feel free to reach out to our author(s)
- [@pannsr](https://www.github.com/pannsr) - pannsr@cs.stanford.edu 


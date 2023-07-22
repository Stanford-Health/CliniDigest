import csv
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
import re

def read_csv_to_dict(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        columns = {header: [] for header in headers}

        for row in reader:
            for header, value in zip(headers, row):
                columns[header].append(value)

    return columns

def string_to_vector(vectorize_type, string_inputs):
  string_inputs = [re.sub(r'\d+', '', s) for s in string_inputs] # get rid of numbers
  if vectorize_type == "tfidf":
    tfidf_vectorizer = TfidfVectorizer(analyzer='word',stop_words= 'english')
    input_vectors = tfidf_vectorizer.fit_transform(string_inputs)
    input_vectors = input_vectors.toarray()

  if vectorize_type == "bow":
    bow_vectorizer = CountVectorizer(analyzer= 'word', stop_words='english')
    input_vectors = bow_vectorizer.fit_transform(string_inputs)
    input_vectors = input_vectors.toarray()
  return input_vectors


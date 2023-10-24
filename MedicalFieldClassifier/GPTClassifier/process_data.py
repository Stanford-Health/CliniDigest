import csv

def read_csv_to_dict(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        columns = {header: [] for header in headers}

        for row in reader:
            for header, value in zip(headers, row):
                columns[header].append(value)

    return columns
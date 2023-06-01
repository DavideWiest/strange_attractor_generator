import csv

import pandas as pd
import chardet


def insert_file_as_column(file_path, csv_file, colname):
    # Read the file contents
    data = read_floats_from_file(file_path)
    lines = [str(l) for l in data]

    # Read the existing CSV file
    with open(csv_file, 'r') as file:
        reader = csv.reader(file)
        rows = list(reader)

    rows[0].insert(-1, colname)

    # Insert the file contents as the second last column in each row
    for i, row in enumerate(rows):
        if i == 0: continue
        row.insert(-1, lines[i-1])

    # Write the updated rows to the CSV file
    with open(csv_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

def read_floats_from_file(filename):
    floats = []
    with open(filename, 'rb') as file:
        raw_data = file.read()
        encoding = chardet.detect(raw_data)['encoding']
        decoded_data = raw_data.decode(encoding)
        for line in decoded_data.splitlines():
            try:
                value = float(line.strip())
                floats.append(value)
            except ValueError:
                pass
    return floats

# Example usage
fileNames = [("vectordirection.txt", "vectorDirection"), ("pixelcount.txt", "graphPixelCount"), ("distance.txt", "medianDistance")]
for f in fileNames:
    insert_file_as_column("data/" + f[0], 'data/train_1k_Reg_simplified.csv', f[1])

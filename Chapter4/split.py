import csv
import random

def split_csv(input_file, train_file, test_file, split_ratio=0.8, random_seed=None):
    """Split a CSV file into training and testing files."""
    if random_seed:
        random.seed(random_seed)

    with open(input_file, 'r', newline='') as f_input:
        csv_reader = csv.reader(f_input)
        header = next(csv_reader)
        data = list(csv_reader)

    random.shuffle(data)
    split_index = int(len(data) * split_ratio)

    train_data = data[:split_index]
    test_data = data[split_index:]

    with open(train_file, 'w', newline='') as f_train:
        csv_writer = csv.writer(f_train)
        csv_writer.writerow(header)
        csv_writer.writerows(train_data)

    with open(test_file, 'w', newline='') as f_test:
        csv_writer = csv.writer(f_test)
        csv_writer.writerow(header)
        csv_writer.writerows(test_data)

# Example usage
input_file = 'imdb_top_1000.csv'  # Replace 'data.csv' with the path to your CSV file
train_file = 'split_train_data.csv'
test_file = 'split_test_data.csv'
split_ratio = 0.9  # 80% training data, 20% testing data
random_seed = 42

split_csv(input_file, train_file, test_file, split_ratio, random_seed)


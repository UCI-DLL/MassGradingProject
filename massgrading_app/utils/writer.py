import os
import csv
import json


def csv_write(dir_path, data):
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    file_path = os.path.join(dir_path, "grading_result.csv")
    file_exists = os.path.isfile(file_path)

    # justify data format
    for key, val in data.items():
        if isinstance(val, list):
            data[key] = " ".join(val)

    with open(file_path, mode='a', newline='') as csv_file:
        writer = csv.writer(csv_file)

        if not file_exists:
            writer.writerow(data.keys())
        writer.writerow(data.values())


def exec_log_write(dir_path, data):
    if not dir_path:
        return
    if not os.path.exists(dir_path):
        os.mkdir(dir_path)

    file_path = os.path.join(dir_path, "execution_log.log")
    with open(file_path, mode="a", newline='\n') as f:
        if isinstance(data, dict):
            f.write(json.dumps(data, indent=4))
            f.write('\n')
        else:
            f.write(data)


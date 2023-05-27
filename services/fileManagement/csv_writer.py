import logging
import csv
from utils.constants import DEFAULT_CSV_HEADER

logger = logging.getLogger()
logger.setLevel(logging.INFO)


class McqCsvWriter:
    def __int__(self, csv_file_path, header=DEFAULT_CSV_HEADER):
        csv_file = open(csv_file_path, 'w', newline='', encoding='UTF-8', errors='ignore')
        self.writer = csv.DictWriter(csv_file, fieldnames=header)
        self.writer.writeheader()

    def write_to_csv(self, row_dict):
        self.writer.writerow(row_dict)
